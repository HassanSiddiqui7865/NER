#!/usr/bin/env python3
"""Install MED7 model from Hugging Face or Dropbox"""
import urllib.request
import zipfile
import tarfile
import os
import site
import sys

def install_from_huggingface():
    """Download and install MED7 model from Hugging Face wheel"""
    model_url = 'https://huggingface.co/kormilitzin/en_core_med7_lg/resolve/main/en_core_med7_lg-any-py3-none-any.whl'
    temp_file = '/tmp/model.whl'
    
    print("Downloading MED7 model from Hugging Face...")
    urllib.request.urlretrieve(model_url, temp_file)
    
    print("Extracting model...")
    site_packages = site.getsitepackages()[0]
    
    with zipfile.ZipFile(temp_file, 'r') as z:
        z.extractall(site_packages)
    
    print("Cleaning up...")
    os.remove(temp_file)
    
    print("Model installed successfully!")
    return site_packages

def install_from_dropbox():
    """Download and install MED7 model from Dropbox (spaCy v2, but may work with v3)"""
    model_url = 'https://www.dropbox.com/s/xbgsy6tyctvrqz3/en_core_med7_lg.tar.gz?dl=1'
    temp_file = '/tmp/model.tar.gz'
    
    print("Downloading MED7 model from Dropbox...")
    urllib.request.urlretrieve(model_url, temp_file)
    
    print("Extracting model...")
    site_packages = site.getsitepackages()[0]
    
    with tarfile.open(temp_file, 'r:gz') as tar:
        tar.extractall(site_packages)
    
    print("Cleaning up...")
    os.remove(temp_file)
    
    print("Model installed successfully!")
    return site_packages

if __name__ == '__main__':
    try:
        # Try Hugging Face first
        print("Attempting to install from Hugging Face...")
        try:
            install_from_huggingface()
        except Exception as e:
            print(f"Hugging Face installation failed: {e}")
            print("Trying Dropbox as fallback...")
            install_from_dropbox()
    except Exception as e:
        print(f"Error installing model: {e}")
        sys.exit(1)
