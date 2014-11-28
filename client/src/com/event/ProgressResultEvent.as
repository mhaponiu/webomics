package com.event
{ 
	import flash.events.Event; 
	
	public class ProgressResultEvent extends Event
	{ 
		public static const TYPE:String = "PROGRESS_RESULT_EVENT";
		
		private var result:Object;
		
		public function ProgressResultEvent(res:Object) 
		{ 
			super(TYPE);
			result = res;
		} 
		
		public function getResult() : Object 
		{
			return result;
		}
	} 
} 