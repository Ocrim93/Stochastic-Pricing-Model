#include "Greeks.h"
#include "./PartialDerivatives.h"

Greeks::Greeks( PayOff* PayOffObject_) : PayOffObject(PayOffObject_)
{	
	params = {PayOffObject->Expiry,
			  PayOffObject->Spot,
			  PayOffObject->Vol,
			  PayOffObject->r};

	step_size_map={{"Expiry", 1e-3},
				  {"Spot", 1.e-2*(PayOffObject->Spot)},				
				  {"Vol", 1e-2},
				  {"r", 1e-2 } };	
}

std::map<std::string,double> Greeks::compute_Greeks()  
{	
	std::map<std::string,double> result ;	
	auto func = [this](double Expiry, double Spot, double Vol, double r){
		//std::cout<< Expiry <<  " "  << Spot <<  " "  << Vol << " "  << r << std::endl;
		return PayOffObject->Value(Expiry,Spot,Vol,r);
	};
	PartialDerivatives<decltype(func), double, double, double, double > DerivativeObject(func);
	
	//double delta = DerivativeObject.first_compute<1>(params,'C', step_size_map["Spot"] );
	double delta = 0 ;
	double gamma = 0;
	double theta = 0 ;
	double vega = 0 ;
	double rho = 0 ;
	//double gamma = DerivativeObject.second_compute<1>(params,step_size_map["Spot"]);
	//double theta = DerivativeObject.first_compute<0>(params,'F',step_size_map["Expiry"]);
	//double vega = DerivativeObject.first_compute<2>(params,'F', step_size_map["Vol"] );
	//double rho = DerivativeObject.first_compute<3>(params,'F', step_size_map["r"]) ;
	int n = 25;
	for (int i = 0; i< n; ++i)
	{
		delta += DerivativeObject.first_compute<1>(params,'C', step_size_map["Spot"] )/n;
		gamma += DerivativeObject.second_compute<1>(params,step_size_map["Spot"])/n;
		theta += DerivativeObject.first_compute<0>(params,'F',step_size_map["Expiry"])/n;
		vega += DerivativeObject.first_compute<2>(params,'F', step_size_map["Vol"] )/n;
		rho += DerivativeObject.first_compute<3>(params,'F', step_size_map["r"])/n;
	}

	result["Delta"] = delta;
	result["Gamma"] = gamma;
	result["Theta"] = theta;
	result["Vega"] = vega;
	result["Rho"] = rho	;
	
	return result;
	
}
