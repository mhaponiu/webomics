package com.event
{
	import flash.events.Event;
	
	public class NewOrganismEvent extends Event
	{
		public static const TYPE :String = "NEW_ORGANISM_EVENT";
		
		public function NewOrganismEvent(id : int, name : String, description : String)
		{
			super(TYPE);
			id_ = id;
			name_ = name;
			description_ = description;
		}
		
		public function getID() : int 
		{
			return id_;
		}
		
		public function getName() : String 
		{
			return name_;
		}
		
		public function getDescription() : String 
		{
			return description_;
		}
		
		private var id_ : int;
		private var name_ : String;
		private var description_ : String;
	}
}
