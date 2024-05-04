echo "Installing required packages ..."

brew install ffmpeg

pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/macosx/arm64/nightly