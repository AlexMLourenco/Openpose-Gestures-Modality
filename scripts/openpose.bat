


echo off
set arg1=%1
set arg2=%2
set arg3=%3
echo on

cd %arg1%
echo "Running OpenPose..." %arg2% %arg3%
cd %arg1%
bin\OpenPoseDemo.exe --hand --image_dir %arg2% --net_resolution 112x112 -write_json %arg3% -display 0 --render_pose 0