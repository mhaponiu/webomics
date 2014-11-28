package com.vos
{
	import flashx.textLayout.formats.Float;

	[RemoteClass (alias="com.vos.ContigVO")]
	[Bindable]
	public class ContigVO extends Object
	{
		public var id:int;
		public var scaff_id:String;
		
		public var order:int;

		public var start:int;
		public var end:int;
		
		public var sequence:String;
		
		public var length_bp:Number;
		
		public function ContigVO(id:int, scaff_id:String, order:int, start:int, end:int, sequence:String, length_bp:Number)
		{
			this.id = id;
			this.scaff_id = scaff_id;
			this.order = order;
			this.start = start;
			this.end = end;
			this.sequence = sequence;
			
			this.length_bp = length_bp;
		}
	}
}