package com.event
{
	import flash.events.Event;
	
	public class OpenOrganismEvent extends Event
	{
		public static const TYPE :String = "OPEN_ORGANISM_EVENT";
		
		public function OpenOrganismEvent(id : String)
		{
			super(TYPE);
			id_ = id;
		}
		
		public function getID() : String 
		{
			return id_;
		}
		
		private var id_ : String;
	}
}
