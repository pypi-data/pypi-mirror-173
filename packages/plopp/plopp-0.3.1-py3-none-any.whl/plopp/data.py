# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Scipp contributors (https://github.com/scipp)

import numpy as np
import scipp as sc

dim_list = ['xx', 'yy', 'zz', 'time', 'temperature']


def scalar_variable(with_variance=False, dtype='float64', unit='m/s'):
    var = sc.scalar(10.0 * np.random.rand(), unit=unit, dtype=dtype)
    if with_variance:
        var.variance = np.random.rand()
    return var


def array_variable(ndim=1, with_variance=False, dims=None, dtype='float64', unit='m/s'):

    shapes = np.arange(50, 0, -10)[:ndim]
    if dims is None:
        dims = dim_list[:ndim][::-1]

    axes = [np.arange(shape, dtype=np.float64) for shape in shapes]
    pos = np.meshgrid(*axes, indexing='ij')
    radius = np.linalg.norm(np.array(pos), axis=0)
    a = np.sin(radius / 5.0)

    var = sc.array(dims=dims, values=a, unit=unit, dtype=dtype)
    if with_variance:
        var.variances = np.abs(np.random.normal(a * 0.1, 0.05))

    return var


def scalar_data_array(with_variance=False,
                      label=False,
                      mask=False,
                      attr=False,
                      dtype='float64',
                      unit='m/s'):

    data = scalar_variable(with_variance=with_variance, dtype=dtype, unit=unit)

    coord_dict = {'xx': scalar_variable(dtype=dtype, unit=unit)}
    attr_dict = {}
    mask_dict = {}

    if label:
        coord_dict["lab"] = scalar_variable(dtype=dtype, unit=unit)
    if attr:
        attr_dict["attr"] = scalar_variable(dtype=dtype, unit=unit)
    if mask:
        mask_dict["mask"] = scalar_variable(dtype=dtype, unit=unit)

    return sc.DataArray(data=data, coords=coord_dict, attrs=attr_dict, masks=mask_dict)


def dense_data_array(ndim=1,
                     with_variance=False,
                     binedges=False,
                     labels=False,
                     masks=False,
                     attrs=False,
                     ragged=False,
                     dims=None,
                     dtype='float64',
                     unit='m/s'):

    coord_units = dict(zip(dim_list, ['m', 'm', 'm', 's', 'K']))

    data = array_variable(ndim=ndim,
                          with_variance=with_variance,
                          dims=dims,
                          dtype=dtype,
                          unit=unit)

    coord_dict = {
        data.dims[i]: sc.arange(data.dims[i],
                                data.shape[i] + binedges,
                                unit=coord_units[data.dims[i]],
                                dtype=np.float64)
        for i in range(ndim)
    }
    attr_dict = {}
    mask_dict = {}

    if labels:
        coord_dict["lab"] = sc.linspace(data.dims[0],
                                        101.,
                                        105.,
                                        data.shape[0],
                                        unit='s')
    if attrs:
        attr_dict["attr"] = sc.linspace(data.dims[0], 10., 77., data.shape[0], unit='s')
    if masks:
        mask_dict["mask"] = sc.array(dims=data.dims,
                                     values=np.where(data.values > 0, True, False))

    if ragged:
        grid = []
        for i, dim in enumerate(data.dims):
            if binedges and (i < ndim - 1):
                grid.append(coord_dict[dim].values[:-1])
            else:
                grid.append(coord_dict[dim].values)
        mesh = np.meshgrid(*grid, indexing="ij")
        coord_dict[data.dims[-1]] = sc.array(dims=data.dims,
                                             values=mesh[-1] +
                                             np.indices(mesh[-1].shape)[0])
    return sc.DataArray(data=data, coords=coord_dict, attrs=attr_dict, masks=mask_dict)


def dense_dataset(entries=None, **kwargs):
    if entries is None:
        entries = ['a', 'b']
    ds = sc.Dataset()
    for entry in entries:
        ds[entry] = (10.0 * np.random.rand()) * dense_data_array(**kwargs)
    return ds


def scatter_data(npoints=500, scale=10.0, seed=1):
    rng = np.random.default_rng(seed)
    position = scale * rng.standard_normal(size=[npoints, 3])
    values = np.linalg.norm(position, axis=1)
    vec = sc.vectors(dims=['row'], unit='m', values=position)
    return sc.DataArray(data=sc.array(dims=['row'], values=values, unit='K'),
                        coords={
                            'position': vec,
                            'x': vec.fields.x,
                            'y': vec.fields.y,
                            'z': vec.fields.z
                        })
