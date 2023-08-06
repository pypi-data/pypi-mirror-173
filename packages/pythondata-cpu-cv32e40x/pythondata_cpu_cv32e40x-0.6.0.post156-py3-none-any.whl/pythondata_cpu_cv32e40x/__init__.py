import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.6.0.post156"
version_tuple = (0, 6, 0, 156)
try:
    from packaging.version import Version as V
    pversion = V("0.6.0.post156")
except ImportError:
    pass

# Data version info
data_version_str = "0.6.0.post14"
data_version_tuple = (0, 6, 0, 14)
try:
    from packaging.version import Version as V
    pdata_version = V("0.6.0.post14")
except ImportError:
    pass
data_git_hash = "93bf5453d9d87bcc24983f562c33a368ba9cfbf4"
data_git_describe = "0.6.0-14-g93bf5453"
data_git_msg = """\
commit 93bf5453d9d87bcc24983f562c33a368ba9cfbf4
Merge: 642cfb2f badde443
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Thu Oct 27 12:59:10 2022 +0200

    Merge pull request #692 from silabs-oysteink/silabs-oysteink_minhv-cherry-pick
    
    Merge minhv handling from CV32E40S

"""

# Tool version info
tool_version_str = "0.0.post142"
tool_version_tuple = (0, 0, 142)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post142")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
