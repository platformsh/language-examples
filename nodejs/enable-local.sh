# You can't run this as its own executable. Instead, source it:
# ENV=pr-XX source enable-local.sh

platform tunnel:open -e $ENV -A nodejs
export PLATFORM_RELATIONSHIPS="$(platform tunnel:info -e $ENV -A nodejs --encode)"
export PLATFORM_ROUTES="$(platform ssh -e $ENV -A nodejs 'echo $PLATFORM_ROUTES' 2&>/dev/null)"

export PLATFORM_APPLICATION_NAME=nodejs
export PLATFORM_ENVIRONMENT=$ENV
export PORT=8888
