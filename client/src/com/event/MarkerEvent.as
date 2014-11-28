package com.event
{ 
	import flash.events.Event; 
	
	public class MarkerEvent 
	{ 
		public function MarkerEvent  () 
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