#ifndef GREEKS_H
#define GREEKS_H
#include <tuple>
#include <map>
#include <string>


class Greeks {
	public:
		Greeks( PayOff* PayOffObject_);
		~Greeks(){};

		std::map<std::string,double> compute_Greeks() ;
		
		std::map<std::string, double> step_size_map;

	private:
		PayOff* PayOffObject;
		std::tuple<double,double,double,double> params;
};

#endif //GREEKS_H
