#include <iostream>
//#include "Module/BlackScholes/BlackScholes.h"
#include "Module/Random/Random.cpp"

using namespace std;

int main(){
	std::cout << "Ciao Mirco "<< std::endl;

	double a = GetOneGaussianByBoxMuller();

	std::cout << a;

}