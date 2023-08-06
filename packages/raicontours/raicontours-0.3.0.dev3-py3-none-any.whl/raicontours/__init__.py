# RAi, machine learning solutions in radiotherapy
# Copyright (C) 2021-2022 Radiotherapy AI Holdings Pty Ltd

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# pylint: disable = invalid-name, useless-import-alias

from __future__ import annotations

import pathlib

from typing_extensions import TypedDict

from .tg263 import TG263 as TG263
from ._version import __version__ as __version__, version_info as version_info

_HERE = pathlib.Path(__file__).parent.resolve()
_model_path = _HERE / "model.h5"


class Config(TypedDict):
    """The model configuration"""

    model_path: pathlib.Path
    structures: list[TG263]
    patch_dimensions: tuple[int, int, int]
    encoding_filter_counts: list[int]
    decoding_filter_counts: list[int]
    rescale_slope: float
    rescale_intercept: float
    reduce_block_sizes: list[tuple[int, int, int]]
    levels: dict[TG263, float]


def get_config():
    # By (re)creating cfg within a function, separate cfg instances are
    # protected from mutating each other.
    cfg: Config = {
        "model_path": _model_path,
        "structures": [
            # TG263.Bladder,
            # TG263.Bone_Mandible,
            # TG263.Brain,
            # TG263.Brainstem,
            # TG263.Carina,
            # TG263.Cavity_Oral,
            # TG263.Cochlea_L,
            # TG263.Cochlea_R,
            # TG263.Duodenum,
            # TG263.Esophagus,
            TG263.Eye_L,
            TG263.Eye_R,
            # TG263.Glnd_Adrenal_L,
            # TG263.Glnd_Adrenal_R,
            TG263.Glnd_Lacrimal_L,
            TG263.Glnd_Lacrimal_R,
            # TG263.Glnd_Submand_L,
            # TG263.Glnd_Submand_R,
            # TG263.Heart,
            # TG263.Kidney_L,
            # TG263.Kidney_R,
            # TG263.Larynx,
            TG263.Lens_L,
            TG263.Lens_R,
            # TG263.Liver,
            # TG263.Lung_L,
            # TG263.Lung_R,
            # TG263.Musc_Constrict,
            # TG263.OpticChiasm,
            TG263.OpticNrv_L,
            TG263.OpticNrv_R,
            # TG263.Pancreas,
            # TG263.Parotid_L,
            # TG263.Parotid_R,
            # TG263.Rectum,
            # TG263.SpinalCord,
            # TG263.Spleen,
            # TG263.Stomach,
            # TG263.Trachea,
        ],
        "patch_dimensions": (64, 64, 64),
        "encoding_filter_counts": [32, 64, 128, 256],
        "decoding_filter_counts": [128, 64, 32, 16],
        "rescale_slope": 4000.0,
        "rescale_intercept": -1024.0,
        "reduce_block_sizes": [(2, 4, 4), (1, 2, 2), (1, 1, 1)],
        "levels": {
            TG263.Lens_L: 50,
            TG263.Lens_R: 50,
            # TG263.OpticChiasm: 1,
            TG263.OpticNrv_L: 50,
            TG263.OpticNrv_R: 50,
            TG263.Eye_L: 100,
            TG263.Eye_R: 100,
            TG263.Glnd_Lacrimal_L: 100,
            TG263.Glnd_Lacrimal_R: 100,
            # TG263.Glnd_Submand_L: 100,
            # TG263.Glnd_Submand_R: 100,
            # TG263.Musc_Constrict: 1.5,
            # TG263.Trachea: 80,
            # TG263.Esophagus: 80,
            # TG263.Cochlea_L: 50,
            # TG263.Cochlea_R: 50,
            # TG263.Larynx: 50,
            # TG263.Parotid_L: 70,
            # TG263.Parotid_R: 70,
            # TG263.Bone_Mandible: 110,
            # TG263.Cavity_Oral: 80,
            # TG263.Brainstem: 127.5,
        },
    }

    return cfg


# TODO: Add a "uids used for training" list and use it to verify a DICOM
# file can be used for metric calculation.
