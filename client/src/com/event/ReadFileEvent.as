package com.event
{
	import flash.events.Event;
	
	public class ReadFileEvent extends Event
	{
		public static const TYPE :String = "READ_FILE_EVENT";
		
		public function ReadFileEvent(text : String)
		{
			super(TYPE);
			text_ = text;
		}
		
		public function getText() : String 
		{
			return text_;
		}
		
		private var text_ : String;
	}
}
