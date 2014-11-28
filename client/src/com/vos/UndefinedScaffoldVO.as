package com.vos
{
	import flashx.textLayout.formats.Float;

	[RemoteClass (alias="com.vos.UndefinedScafoldVO")]
	[Bindable]
	public class UndefinedScafoldVO extends Object
	{
		public var id:int;
		public var scaff_id:int;
		public var sequence:String;
		
		public var start_bp:Float;
		public var end_bp:Float;
		
		public var length_all_bp:Float;
		
		public var order:Float;
		public var assemb_type:int;
		
		public function UndefinedScafoldVO(id:String, scaff_id:String, start:Float, end:Float, sequence:String, length_bp:Float, order:Float, assemb_type:int)
		{
			this.id = id;
			this.scaff_id = scaff_id;
			this.sequence = sequence;
			this.start_bp = start;
			this.end_bp = end;
			this.length_all_bp = length_bp;
			this.order = order;
			this.assemb_type = assemb_type;
		}
	}
}