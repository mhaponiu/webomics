package com.vos
{
	import flashx.textLayout.formats.Float;

	[RemoteClass (alias="com.vos.MarkerVO")]
	[Bindable]
	public class MarkerVO extends Object
	{
		public var name:String;
		public var chr_id:int;
		public var pos_cm:Number;
		public var cont_id:int;
		public var contig_start:Number;
		public var contig_end:Number;
		public var scaff_id:String;
		public var scaffold_start:Number;
		public var scaffold_end:Number;
		public var sequence:String;
		
		public function MarkerVO(name:String, chr_id:int, pos_cm:Number, cont_id:int, contig_start:Number, contig_end:Number, scaff_id:String, scaffold_start:Number, scaffold_end:Number, sequence:String)
		{
			this.name = name;
			this.chr_id = chr_id;
			this.pos_cm = pos_cm;
			this.cont_id = cont_id;
			this.contig_start = contig_start;
			this.contig_end = contig_end;
			this.scaff_id = scaff_id;
			this.scaffold_start = scaffold_start;
			this.scaffold_end = scaffold_end;
			this.sequence = sequence;
		}
	}
}