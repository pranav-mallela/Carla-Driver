cmake_minimum_required(VERSION 3.0.2)
project(orb_slam)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  cv_bridge
  image_transport
  tf
  sensor_msgs
)

# Keep compiler flags and checks
IF(NOT CMAKE_BUILD_TYPE)
  SET(CMAKE_BUILD_TYPE Release)
ENDIF()

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS}  -Wall  -O3 -march=native ")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall  -O3 -march=native")

# Check C++11 support
include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
CHECK_CXX_COMPILER_FLAG("-std=c++0x" COMPILER_SUPPORTS_CXX0X)
if(COMPILER_SUPPORTS_CXX11)
   set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
   add_definitions(-DCOMPILEDWITHC11)
elseif(COMPILER_SUPPORTS_CXX0X)
   set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
   add_definitions(-DCOMPILEDWITHC0X)
else()
   message(FATAL_ERROR "The compiler ${CMAKE_CXX_COMPILER} has no C++11 support. Please use a different C++ compiler.")
endif()

# Find required packages
find_package(OpenCV 4.4 EXACT REQUIRED)

find_package(Eigen3 3.1.0 REQUIRED)
find_package(Pangolin REQUIRED)
find_package(Sophus REQUIRED)

# Set paths for ORB_SLAM3 dependencies
set(ORB_SLAM3_ROOT_DIR /ORB_SLAM3/)
set(ORB_SLAM3_INCLUDE_DIR ${ORB_SLAM3_ROOT_DIR}/include)
set(DBOW2_LIB_DIR ${ORB_SLAM3_ROOT_DIR}/Thirdparty/DBoW2/lib)
set(G2O_LIB_DIR ${ORB_SLAM3_ROOT_DIR}/Thirdparty/g2o/lib)
set(ORB_SLAM3_LIB_DIR ${ORB_SLAM3_ROOT_DIR}/lib)

# Check if required libraries exist
if(NOT EXISTS ${DBOW2_LIB_DIR}/libDBoW2.so)
    message(FATAL_ERROR "DBoW2 library not found. Please build ORB_SLAM3 first.")
endif()

if(NOT EXISTS ${G2O_LIB_DIR}/libg2o.so)
    message(FATAL_ERROR "g2o library not found. Please build ORB_SLAM3 first.")
endif()

if(NOT EXISTS ${ORB_SLAM3_LIB_DIR}/libORB_SLAM3.so)
    message(FATAL_ERROR "ORB_SLAM3 library not found. Please build ORB_SLAM3 first.")
endif()

###################################
## catkin specific configuration ##
###################################
catkin_package(
  INCLUDE_DIRS include
  LIBRARIES ${PROJECT_NAME}
  CATKIN_DEPENDS roscpp std_msgs cv_bridge image_transport tf sensor_msgs
  DEPENDS OpenCV Eigen3 Pangolin
)

###########
## Build ##
###########

include_directories(
  BEFORE
  include
  ${catkin_INCLUDE_DIRS}
  ${ORB_SLAM3_ROOT_DIR}
  ${ORB_SLAM3_INCLUDE_DIR}
  ${ORB_SLAM3_INCLUDE_DIR}/CameraModels
  ${Pangolin_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
  ${Sophus_INCLUDE_DIRS}
)

# Add compile definitions to help with include paths
add_definitions(-DORB_SLAM3_ROOT_DIR="${ORB_SLAM3_ROOT_DIR}")
add_definitions(-DORB_SLAM3_INCLUDE_DIR="${ORB_SLAM3_INCLUDE_DIR}")

set(LIBS 
  ${OpenCV_LIBS} 
  ${EIGEN3_LIBS}
  ${Pangolin_LIBRARIES}
  ${catkin_LIBRARIES}
  ${Sophus_LIBRARIES}
  ${DBOW2_LIB_DIR}/libDBoW2.so
  ${G2O_LIB_DIR}/libg2o.so
  ${ORB_SLAM3_LIB_DIR}/libORB_SLAM3.so
  -lboost_system
)

# Node for monocular camera
add_executable(Mono src/ros_mono.cc)
target_link_libraries(Mono ${LIBS})
add_dependencies(Mono ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

# Node for monocular camera (Augmented Reality Demo)
# add_executable(MonoAR src/AR/ros_mono_ar.cc src/AR/ViewerAR.h src/AR/ViewerAR.cc)
# target_link_libraries(MonoAR ${LIBS})
# add_dependencies(MonoAR ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

# Node for stereo camera
# add_executable(Stereo src/ros_stereo.cc)
# target_link_libraries(Stereo ${LIBS})
# add_dependencies(Stereo ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

# Node for RGB-D camera
add_executable(RGBD src/ros_rgbd.cc)
target_link_libraries(RGBD ${LIBS})
add_dependencies(RGBD ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

# Node for monocular-inertial camera
add_executable(Mono_Inertial src/ros_mono_inertial.cc)
target_link_libraries(Mono_Inertial ${LIBS})
add_dependencies(Mono_Inertial ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

# Node for stereo-inertial camera
add_executable(Stereo_Inertial src/ros_stereo_inertial.cc)
target_link_libraries(Stereo_Inertial ${LIBS})
add_dependencies(Stereo_Inertial ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

# Node for TesterBester
add_executable(TesterBester src/testerbester.cc)
target_link_libraries(TesterBester ${LIBS})
add_dependencies(TesterBester ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

#############
## Install ##
#############

# Mark executables for installation
# install(TARGETS Mono MonoAR Stereo RGBD Mono_Inertial Stereo_Inertial TesterBester)
install(TARGETS TesterBester Mono Mono_Inertial RGBD
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# Mark launch and config files for installation
install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
  FILES_MATCHING PATTERN "*.launch"
)
