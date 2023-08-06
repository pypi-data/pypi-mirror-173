import tempfile
from pathlib import Path
import gzip
import shutil
import numpy as np
import nibabel as nb


def get_image(
    out_file: Path = None,
    data: np.ndarray = None,
    vox_sizes=(1.0, 1.0, 1.0),
    qform=(1, 2, 3, 1),
    compressed=False,
) -> Path:
    """Create a random Nifti file to satisfy BIDS parsers"""
    if out_file is None:
        out_file = Path(tempfile.mkdtemp()) / "sample.nii"

    if data is None:
        data = np.random.randint(0, 1, size=[10, 10, 10])

    uncompressed = out_file.with_suffix('.nii')

    hdr = nb.Nifti1Header()
    hdr.set_data_shape(data.shape)
    hdr.set_zooms(vox_sizes)  # set voxel size
    hdr.set_xyzt_units(2)  # millimeters
    hdr.set_qform(np.diag(qform))
    nb.save(
        nb.Nifti1Image(
            data,
            hdr.get_best_affine(),
            header=hdr,
        ),
        uncompressed,
    )

    if compressed:
        out_file = out_file.with_suffix('.nii.gz')
        with open(uncompressed, 'rb') as f_in:
            with gzip.open(out_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    else:
        out_file = uncompressed

    return out_file
