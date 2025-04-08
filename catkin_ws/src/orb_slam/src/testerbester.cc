// Just testing ROSCPP

#include<iostream>
#include<ros/ros.h>

using namespace std;

int main(int argc, char **argv) {
ros::init(argc, argv, "TesterBester");
cout << "Hola" << endl;
ros::shutdown();
return 1;
}


