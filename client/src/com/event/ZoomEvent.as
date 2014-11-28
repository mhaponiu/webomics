package com.event
{
	import flash.events.Event;
	
	public class ZoomEvent extends Event
	{
		public static const TYPE :String = "ZOOM_EVENT";
		
		public function ZoomEvent(start : Object, stop : Object)
		{
			super(TYPE);
			start_ = int(start);
			stop_ = int(stop);
		}
		
		public function getStart() : int 
		{
			return start_;
		}
		
		public function getStop() : int 
		{
			return stop_;
		}
		
		private var start_ : int;
		private var stop_ : int;
	}
}
