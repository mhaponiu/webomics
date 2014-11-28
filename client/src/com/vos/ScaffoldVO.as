package com.vos
{
	import flashx.textLayout.formats.Float;

	[RemoteClass (alias="com.vos.ScaffoldVO")]
	[Bindable]
	public class ScaffoldVO extends Object
	{
		public var id:String;
		public var scaff_id:String;
		public var chromosome_id:int;
		public var sequence:String;
		public var assemb_type:int;
		
		public var start:Float;
		public var end:Float;
		
		public var color:String;
		
		public var order:int;
		
		public var length_bp:Float;
		
		public function ScaffoldVO(id:String, scaff_id:String, chromosome_id:int, start:Float, end:Float, sequence:String, assemb_type:int, color:String, order:int, length_bp:Float)
		{
			this.id = id;
			this.scaff_id = scaff_id;
			this.chromosome_id = chromosome_id;
			this.sequence = sequence;
			this.assemb_type = assemb_type;
			this.start = start;
			this.end = end;
			this.color = color;
			this.order = order;
			this.length_bp = length_bp;
		}
	}
}