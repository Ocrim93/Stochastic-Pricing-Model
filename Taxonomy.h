#ifndef TAXONOMY_H
#define TAXONOMY_H

#include <map>

enum class UnderlyingName{ VOLATILITY, INTEREST_RATE, SPOT, EXPIRY 	};

char GetUnderlyingToChar(UnderlyingName u)
{
 	std::map<UnderlyingName,char> UnderlyingToChar = 
 		{{UnderlyingName::VOLATILITY, 'V'},
		 {UnderlyingName::INTEREST_RATE, 'I'},
		 {UnderlyingName::SPOT, 'S'},
		 {UnderlyingName::EXPIRY, 'E'}
		};
	return UnderlyingToChar[u];
}

#endif