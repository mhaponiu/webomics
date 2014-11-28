package com.event
{
	import flash.events.Event;
	
	public class DeleteOrganismEvent extends Event
	{
		public static const TYPE :String = "DELETE_ORGANISM_EVENT";
		
		public function DeleteOrganismEvent(id : int)
		{
			super(TYPE);
			id_ = id;
		}
		
		public function getID() : int 
		{
			return id_;
		}
		
		private var id_ : int;
	}
}
