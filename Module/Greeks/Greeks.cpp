#include "Greeks.h"
#include "./PartialDerivatives.h"

Greeks::Greeks( PayOff* PayOffObject_) : PayOffObject(PayOffObject_)
{	
	step_size = 1.e-4;
	params = {PayOffObject->Expiry,
			  PayOffObject->Spot,
			  PayOffObject->Vol,
			  PayOffObject->r};

}

std::map<std::string,double> Greeks::compute_Greeks() const 
{	
	std::map<std::string,double> result ;	
	auto func = [this](double Expiry, double Spot, double Vol, double r){
		return PayOffObject->Value(Expiry,Spot,Vol,r);
	};
	PartialDerivatives<decltype(func), double, double, double, double > DerivativeObject(func, step_size);
	
	double delta = DerivativeObject.first_compute<1>(params,'C');
	double gamma = DerivativeObject.second_compute<1>(params);
	double theta = DerivativeObject.first_compute<0>(params,'F');
	double vega = DerivativeObject.first_compute<2>(params,'F');
	double rho = DerivativeObject.first_compute<3>(params,'C');

	result["Delta"] = delta;
	result["Gamma"] = gamma;
	result["Theta"] = theta;
	result["Vega"] = vega;
	result["Rho"] = rho;

	return result;
	
}

void Greeks::SetStepSize(double StepSize_)
{
	step_size =  StepSize_;
}