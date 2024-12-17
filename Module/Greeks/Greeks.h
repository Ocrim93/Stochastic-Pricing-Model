#ifndef GREEKS_H
#define GREEKS_H
//#include "../Payoff/Payoff.cpp"
#include <tuple>
#include <map>
#include <string>

class Greeks {
	public:
		Greeks( PayOff* PayOffObject_);
		~Greeks(){};

		std::map<std::string,double> compute_Greeks() const;
		
		double step_size;
		void SetStepSize(double StepSize_);

	private:
		PayOff* PayOffObject;
		std::tuple<double,double> params;
};

#endif //GREEKS_H
