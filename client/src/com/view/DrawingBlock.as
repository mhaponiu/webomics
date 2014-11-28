package com.view
{
	public class DrawingBlock extends Object
	{
		public var used:Boolean = false;
		public var text:String = "";
		public var padding_top:int = 0;

		public function DrawingBlock(used:Boolean, text:String, padding_top:int)
		{
			this.used = used;
			this.text = text;
			this.padding_top = padding_top;
		}
	}
}