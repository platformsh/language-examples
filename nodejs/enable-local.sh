# You can't run this as its own executable. Instead, source it:
# ENV=pr-XX source enable-local.sh

platform tunnel:open -e $ENV -A nodejs
export PLATFORM_RELATIONSHIPS="$(platform tunnel:info -e $ENV -A nodejs --encode)"

export PLATFORM_APP_NAME=nodejs
export PORT=8888
