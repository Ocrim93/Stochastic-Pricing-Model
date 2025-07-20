#include <iostream>
#include "Payoff/Vanilla/Vanilla.cpp"
#include <tuple>
#include <string>
#include <map>
#include <stdio.h>
using namespace std;

int main(){

	std::cout << "Ciao Mirco "<< std::endl;
	double Expiry = 1;
	double Strike = 245	;
	double Spot = 250;
	double Vol = 0.2;
	double r = 0.04 ;
	double q = 0.4/100;
	unsigned long NumberOfPaths = 1e6;
	q = 0;
	VanillaCall call(Strike,Expiry,Spot ,Vol,r, q );
	double value;
	//basePayoff =  VanillaCall(Strike,Expiry);
	value = call.Value();

	//double implVolBis = call.ImpliedVolBisection(25,0.1,0.3);
	//double NR = call.ImpliedVolNewtonRaphson(25,0.1);

	std::cout << "Price : "<<value<< std::endl;
	//std::cout << "Bisection Impl Vol : "<<implVolBis<< std::endl;
	//std::cout << "Implied Vol NewtonRaphson : "<<NR<< std::endl;

	std::map<std::string,double> hedging_greeks = call.Hedging_Greeks() ;
	for (auto &  t : hedging_greeks)	
		{	
			std::cout << t.first << " : "<< t.second << std::endl;
		} 

	VanillaCall call_f(Strike,Expiry,Spot + 0.01*Spot  ,Vol,r, q );
	double value_f = call_f.Value();
	std::cout << "Price_f : "<<value_f<< std::endl;

	std::cout<< (value_f - value)/(0.01*Spot) << std::endl;
	

}