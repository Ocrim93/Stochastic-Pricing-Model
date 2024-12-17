#include <iostream>
#include "Module/Payoff/Vanilla/Vanilla.cpp"
#include <tuple>
using namespace std;

int main(){

	std::cout << "Ciao Mirco "<< std::endl;
	double Expiry = 1;
	double Strike = 55;
	double Spot = 50;
	double Vol = 0.2;
	double r = 0.03 ;
	double q = 0.4/100;
	unsigned long NumberOfPaths = 1e6;
	VanillaCall call(Strike,Expiry,Spot ,Vol,r, q );
	double value;
	//basePayoff =  VanillaCall(Strike,Expiry);
	value = call.Value();

	//double implVolBis = call.ImpliedVolBisection(2.12,0,0.3);
	//double NR = call.ImpliedVolNewtonRaphson(2.12,0.2);

	std::cout << value<< std::endl;
	//std::cout << implVolBis<< std::endl;
	//std::cout << NR<< std::endl;
	/*
	auto fun = [](double x, double y) -> double {
		return x*x*x + y*y;
	};
	double h = 1.e-4;
	tuple<double,double> point(3.,4.);
	int dir = 1;

	PartialDerivatives<decltype(fun), double,double>  pd(fun, h);
	double v = pd.first_compute<0>(point);
	std::cout << v<< std::endl;
*/
    }