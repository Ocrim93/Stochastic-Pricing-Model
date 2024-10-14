#include <iostream>
#include "Module/BlackScholes/BlackScholes.cpp"
#include "Module/Random/Random.cpp"

using namespace std;

int main(){

	int x = 5;

	const int*   p = &x;
	std::cout<< *p << "    " <<x << "       "<< p<< std::endl;
	*p = 10;
	std::cout<< *p << "    " <<x << "       "<< p<< std::endl;
	std::cout << "Ciao Mirco "<< std::endl;
	double Expiry = 1;
	double Strike = 55;
	double Spot = 50;
	double Vol = 0.2;
	double r = 0.03 ;
	double q = 0.4/100;
	unsigned long NumberOfPaths = 100000;
	double a = GetOneGaussianByBoxMuller();

	double call = BlackScholesPathIndependent(  Expiry,
									 Strike,
									 Spot,
									 Vol,
									 r,
									 q,
									  NumberOfPaths);

	std::cout << a<< std::endl;
	std::cout << call<< std::endl;


}