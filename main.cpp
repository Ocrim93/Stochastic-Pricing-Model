#include <iostream>
#include "Module/BlackScholes/BlackScholes.cpp"
#include "Module/Random/Random.cpp"
#include "Module/Payoff/Payoff.cpp"

using namespace std;

int main(){


	std::cout << "Ciao Mirco "<< std::endl;
	double Expiry = 1;
	double Strike = 55;
	double Spot = 50;
	double Vol = 0.2;
	double r = 0.03 ;
	double q = 0.4/100;
	unsigned long NumberOfPaths = 100000;
	double a = GetOneGaussianByBoxMuller();
	PayOff* basePayoff;
	basePayoff = new PayOffCall(Strike);
	double call = BlackScholesPathIndependent( *basePayoff,
									  Expiry,
									 Spot,
									 Vol,
									 r,
									 q,
									  NumberOfPaths);

	std::cout << a<< std::endl;
	std::cout << call<< std::endl;


}