import os
import platform
import shutil
import tempfile

CMGEN_FILEPATH = {
    "Windows": "../tools/win32/cmgen.exe",
    "Darwin": "../tools/macos/cmgen",
    "Linux": "../tools/linux/cmgen",
}

LOOKUP_COMMAND = "{cmgen} --ibl-dfg={filepath}.hdr"
DIFFUSE_COMMAND = "{cmgen} --format=hdr --ibl-irradiance={directory} {filepath}"
SPECULAR_COMMAND = "{cmgen} --format=hdr --size=512 --ibl-ld={directory} {filepath}"


def _get_cmgen_path():
    system_name = platform.system()
    cmgen_path = CMGEN_FILEPATH[system_name]
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, cmgen_path)


def gen_environment_maps(input_file, output_dir):
    cmgen_path = _get_cmgen_path()
    temp_dir = tempfile.mkdtemp()
    diffuse_command = DIFFUSE_COMMAND.format(
        cmgen=cmgen_path, directory=temp_dir, filepath=input_file
    )
    specular_command = SPECULAR_COMMAND.format(
        cmgen=cmgen_path, directory=temp_dir, filepath=input_file
    )
    os.system(diffuse_command)
    os.system(specular_command)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_name = os.path.splitext(os.path.basename(input_file))[0]
    cubemap_dir = os.path.join(temp_dir, input_name)
    for filename in os.listdir(cubemap_dir):
        src_filepath = os.path.join(cubemap_dir, filename)
        dst_filepath = os.path.join(output_dir, filename)
        shutil.copyfile(src_filepath, dst_filepath)
    shutil.rmtree(temp_dir)


def gen_lookup_texture(filepath):
    cmgen_path = _get_cmgen_path()
    command = LOOKUP_COMMAND.format(cmgen=cmgen_path, filepath=filepath)
    os.system(command)
