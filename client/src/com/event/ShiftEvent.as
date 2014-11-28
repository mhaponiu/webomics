package com.event
{
	import flash.events.Event;
	
	public class ShiftEvent extends Event
	{
		public static const TYPE :String = "SHIFT_EVENT";
		
		public function ShiftEvent(shift : Object)
		{
			super(TYPE);
			shift_ = int(shift);
		}
		
		public function getShift() : int 
		{
			return shift_;
		}
		
		private var shift_ : int;
	}
}
