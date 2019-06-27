#include <iostream>
#include <sstream>
#include <fstream>
//#include <boost/regex.hpp>
//#include <boost/date_time/posix_time/posix_time.hpp>
#include <ros/ros.h>
#include "rospeex_if/rospeex.h"
#include <string>
#include <time.h>
#include <stdio.h>

static rospeex::Interface interface;
static int number = 0;

void sr_response( const std::string& msg )
{
	//using boost::posix_time::ptime;
	//using boost::posix_time::second_clock;

	std::string msg_w = msg;
	std::cerr << "you said : " << msg << std::endl;

	std::ofstream ofs;
	char fname[128];
	sprintf(fname, "/home/emlab/words_functions/text%d.txt", number);
	ofs.open(fname, std::ios::trunc);
	ofs << msg_w << std::flush;
	ofs.close();

	std::ofstream ofs_t;
	time_t current;
	struct tm *local;
	time(&current);
	local = localtime(&current);

	char fname_t[128];
	sprintf(fname_t, "/home/emlab/words_functions/time%d.txt", number);
	ofs_t.open(fname_t, std::ios::trunc);
	ofs_t << local->tm_hour << "h " << local->tm_min << "m " << local->tm_sec << "s" << std::flush;
	ofs_t.close();

	number += 1;
	std::cerr << "REC OK" << std::endl;
	
}

int main( int argc, char** argv )
{
	ros::init(argc, argv, "sr_ss_demo");

	interface.init();
	interface.registerSRResponse( sr_response );
	interface.setSPIConfig("ja", "nict");
	ros::spin();
	return 0;
}
