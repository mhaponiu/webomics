package com.event
{ 
	import flash.events.Event; 
	
	public class ContigEvent 
	{ 
		public function ContigEvent () 
		{ 
		} 
		
		public static function informations(method:Function, additionalArguments:Array):Function 
		{ 
			return function(event:Event):void 
			{ 
				method.apply(null, [event].concat(additionalArguments)); 
			} 
		} 
	} 
} 