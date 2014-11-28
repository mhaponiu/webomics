package com.event
{
	import flash.events.Event;
	
	public class ImportEvent extends Event
	{
		public static const TYPE :String = "IMPORT_EVENT";
		
		public function ImportEvent()
		{
			super(TYPE);
		}
	}
}
