import os
import configparser


def get_ansible_config_filepath() -> str:
    ansible_cfg_cur_dir_filepath = os.path.abspath("ansible.cfg")
    ansible_cfg_home_dir_filepath = os.path.expanduser("~/.ansible.cfg")
    ansible_etc_filepath = "/etc/ansible/ansible.cfg"
    if "ANSIBLE_CONFIG" in os.environ:
        ansible_config_env_filepath = os.environ["ANSIBLE_CONFIG"]
        if not os.path.exists(ansible_config_env_filepath):
            raise FileNotFoundError()
        return ansible_config_env_filepath
    elif os.path.exists(ansible_cfg_cur_dir_filepath):
        return ansible_cfg_cur_dir_filepath
    elif os.path.exists(ansible_cfg_home_dir_filepath):
        return ansible_cfg_home_dir_filepath
    elif os.path.exists(ansible_etc_filepath):
        return ansible_etc_filepath
    else:
        return ""


def get_dict_of_ansible_config_options() -> dict:
    config_filepath = get_ansible_config_filepath()
    if config_filepath == "":
        return {}
    config = configparser.ConfigParser()
    config.read(config_filepath)
    config_dictionary = {}
    for section in config.sections():
        for option in config.options(section):
            config_dictionary[option] = config.get(section, option)
    return config_dictionary
