import copy
import json
import base64
import pickle
import requests
import itertools
from typing import Any, Tuple
# from multiprocessing.shared_memory import SharedMemory
from .shared_memory import SharedMemory

import torch
import numpy as np

class XMetadata: ...
class XMetaItem: ...

class XMetadata:
    def __init__(self, shmname=None):
        self._shmname = shmname
        self._shmsize = 0
        self._items = []
        self._items_count = []

    def __len__(self):
        return len(self._items)

    def add(self, name: str, shape: Tuple, dtype: Any, nbytes: int):
        self._items.append(XMetaItem(name, shape, dtype, nbytes))
    
    @property
    def shmname(self) -> str:
        return self._shmname
    
    def items(self) -> list[XMetaItem]:
        return self._items

class XMetaItem:
    def __init__(self, name: str, shape: Tuple, dtype: Any, nbytes: int):
        self._name = name
        self._shape = shape
        self._dtype = dtype
        self._nbytes = nbytes
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def shape(self) -> Tuple:
        return self._shape

    @property
    def dtype(self):
        return self._dtype
    
    @property
    def nbytes(self) -> int:
        return self._nbytes

def x_create_shm(addr: str, model: str, tag: str, shmsize: int) -> str:
    url = 'http://{}/shmodels/{}/{}'.format(addr, model, tag)
    req = requests.post(url, data=json.dumps({
        'mem_request': int(shmsize)
    }))
    if req.status_code != 200:
        print('Failed to create SharedModel. [%d] %s' % (req.status_code, req.json()))
        return ''

    return req.json()['data']['shmname']

def x_save_states(model: torch.nn.Module, shmname: str) -> Tuple[SharedMemory, XMetadata]:
    metadata = XMetadata(shmname)

    # Extract tensors from the model
    shmsize = 0
    tensors = []
    for _, module in model.named_modules():
        tensors_module = {'params': [], 'buffers': []}
        for name, param in module.named_parameters(recurse=False):
            t = torch.clone(param).detach().numpy()
            if len(t.shape) <= 0:
                continue
            shmsize += t.nbytes

            metadata.add(name, t.shape, t.dtype, t.nbytes)
            tensors_module['params'].append(t)

        for name, buffer in module.named_buffers(recurse=False):
            t = torch.clone(buffer).detach().numpy()
            if len(t.shape) <= 0:
                continue
            shmsize += t.nbytes

            metadata.add(name, t.shape, t.dtype, t.nbytes)
            tensors_module['buffers'].append(t)

        tensors.append(tensors_module)

    metadata._items_count = [(len(m['params']), len(m['buffers'])) for m in tensors]
    tensors = itertools.chain.from_iterable([it['params'] + it['buffers'] for it in tensors]) # Flatten the nested list

    # Save tensors into the shared memory block
    shm = SharedMemory(shmname, create=False, size=shmsize)
    metadata._shmsize = shmsize
    
    start, end = 0, 0
    for t in tensors:
        end += t.nbytes

        _shmarray = np.ndarray(t.shape, t.dtype, buffer=shm.buf[start:end])
        _shmarray[:] = t[:]
        start = int(end)

    for t in tensors: del t

    return shm, metadata

def x_apply_shm(addr: str, model: str, tag: str, metadata: XMetadata):
    url = 'http://{}/shmodels/{}/{}'.format(addr, model, tag)

    enc = lambda obj: base64.b64encode(pickle.dumps(obj)).decode('ascii')
    req = requests.put(url, data=json.dumps({
        'metadata': enc(metadata)
    }))
    if req.status_code != 200:
        print('Failed to put the metadata. [%d] %s' % (req.status_code, req.json()))
        return

def x_load_states(model: torch.nn.Module, metadata: XMetadata) -> Tuple[SharedMemory, torch.nn.Module]:
    # Make a copy of the given model
    copied_model = copy.deepcopy(model)
    for _, module in copied_model.named_modules():
        for name in [name for name, _ in module.named_parameters(recurse=False)]:
            setattr(module, name, None)
        for name in [name for name, _ in module.named_buffers(recurse=False)]:
            setattr(module, name, None)
    copied_model.train(False)

    # Load tensors from the shared memory block
    shm = SharedMemory(metadata.shmname)

    offset, curr = 0, 0
    items = metadata.items()
    modules = [module for _, module in copied_model.named_modules()]
    for i, module in enumerate(modules):
        param_counts = metadata._items_count[i][0]
        buffer_counts = metadata._items_count[i][1]

        for _ in range(param_counts):
            _item = items[curr]
            _shmarray = np.ndarray(shape=_item.shape, dtype=_item.dtype, buffer=shm.buf[offset:offset+_item.nbytes])
            module.register_parameter(name=_item.name, param=torch.nn.Parameter(torch.from_numpy(_shmarray)))
            offset += _item.nbytes
            curr += 1

        for _ in range(buffer_counts):
            _item = items[curr]
            _shmarray = np.ndarray(shape=_item.shape, dtype=_item.dtype, buffer=shm.buf[offset:offset+_item.nbytes])
            module.register_buffer(name=_item.name, tensor=torch.from_numpy(_shmarray))
            offset += _item.nbytes
            curr += 1

    return shm, copied_model

def x_get_metadata(addr: str, model: str, tag: str) -> XMetadata:
    url = 'http://{}/shmodels/{}/{}'.format(addr, model, tag)
    req = requests.get(url)
    if req.status_code != 200:
        print('Failed to create SharedModel. [%d] %s' % (req.status_code, req.json()['message']))
        return
    
    dec = lambda obj: pickle.loads(base64.b64decode(obj.encode('ascii')))
    metadata = dec(req.json()['data']['metadata'])
    return metadata

def x_calc_bytes(model: torch.nn.Module) -> int:
    shmsize = 0
    for _, module in model.named_modules():
        for _, param in module.named_parameters(recurse=False):
            t = torch.clone(param).detach().numpy()
            shmsize += t.nbytes

        for _, buffer in module.named_buffers(recurse=False):
            t = torch.clone(buffer).detach().numpy()
            t = buffer.numpy()
            shmsize += t.nbytes

    return shmsize