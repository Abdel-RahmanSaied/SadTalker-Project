echo "Installing required packages ..."

apt-get install ffmpeg

pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/macosx/arm64/nightly