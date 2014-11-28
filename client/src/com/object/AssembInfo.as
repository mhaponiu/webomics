package com.object
{
	public class AssembInfo extends Object
	{
		public var assemb_id:uint;
		public var name:String;
		public var position:Number;
		
		public function AssembInfo(assemb_id:uint, name:String, position:Number)
		{
			this.assemb_id = assemb_id;
			this.name = name;
			this.position = position;
		}
	}
}