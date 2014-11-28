package com.view
{
	import com.config.Config;
	import com.dialog.ContigInformations;
	import com.dialog.MarkerInformations;
	import com.event.ContigEvent;
	import com.event.MarkerEvent;
	import com.event.ShiftEvent;
	import com.event.ZoomEvent;
	import com.remote.RemoteControl;
	import com.style.HTMLToolTip;
	import com.view.DrawingBlock;
	import com.vos.ContigVO;
	import com.vos.MarkerVO;
	import com.vos.ScaffoldVO;
	
	import flash.display.Graphics;
	import flash.events.Event;
	import flash.events.KeyboardEvent;
	import flash.events.MouseEvent;
	import flash.net.NetConnection;
	import flash.net.Responder;
	
	import flashx.textLayout.formats.Float;
	
	import mx.collections.ArrayCollection;
	import mx.containers.Box;
	import mx.containers.Canvas;
	import mx.controls.Alert;
	import mx.controls.Label;
	import mx.managers.CursorManager;
	import mx.managers.PopUpManager;
	import mx.managers.ToolTipManager;
	import mx.messaging.AbstractConsumer;
	import mx.rpc.events.FaultEvent;
	import mx.styles.StyleManager;
	import mx.utils.ArrayUtil;

	/**
	 * 
	 * 
	*/
	public class ScaffoldCanvas extends Canvas
	{
		// -------------------------------------------------- ZMIENNE KLASY --------------------------------------------
		
		/**
		 * 
		 */
		private var connection:NetConnection;
		
		/**
		 * 
		 */
		private var interval:Number = new Number();
		
		/**
		 * 
		 */
		private var factor:Number = new Number();
		
		/**
		 * 
		 */
		private var display_from:Number = new Number();
		
		/**
		 * 
		 */
		private var display_to:Number = new Number();
		
		/**
		 * 
		 */
		private var shift_start:Number = new Number();
		
		/**
		 * 
		 */
		private var zoom_start:Number = new Number();
		
		/**
		 * 
		 */
		private var zoom_start_position:Number = new Number();
		
		/**
		 * 
		 */
		private var colors:Array = ["#1811E6", "#E91220", "#09E402"];
		
		/**
		 * 
		 */
		private var current_color:uint = 0;
		
		/**
		 * 
		 */
		private var zoom_box:Box = null;
		
		/**
		 * 
		 */
		private var zoom_end_label:Label = null;
		
		/**
		 * 
		 */
		private var shift_end_label:Label = null;
		
		/**
		 * 
		 */
		private var is_added:Boolean = false;
		
		/**
		 * 
		 */
		private static const POSITIONS_RULER_PADDING_TOP:Number = 1;
		
		// -------------------------------------------------- KONSTRUKTOR ----------------------------------------------
		
		/**
		 * Konstruktor 
		 * @param width:
		 * @param height:
		 * @param from:
		 * @param to:
		 * @param scaff_obj:
		 */
		public function ScaffoldCanvas(width:Number, height:Number, from:Number, to:Number, scaff_obj:Object)
		{
			// Ustawienie menadzera tooltipow
			ToolTipManager.toolTipClass = HTMLToolTip;
			
			// Nawiazanie polaczenia z serwerem aplikacji
			connection = new NetConnection();
			connection.connect(RemoteControl.GATEWAY);
			
			zoom_box = new Box();
			
			// Szerokosc obszaru rysowania
			this.width = width - 20;
			
			// Wysokosc obszaru rysowania
			this.height = height - 20;
			
			// Szerokosci przedzialu
			var length:Number = to - from;
			
			// Obliczenie stalych wartosci
			interval = this.width / length;
			factor = this.width / length;
			display_from = from;
			display_to = to;

			trace("Rozpoczeto budowanie drzewa przedzialowego z contigami...");
			// Zbudowanie drzewa przedzialowego z contigami
			connection.call("contig.buildTree", new Responder(onBuildTree, onFaultBuildTree), scaff_obj.scaff_id);
			
			trace("Rozpoczeto budowanie drzewa przedzialowego z markerami...");
			// Zbudowanie drzewa przedzialowego z markerami
			connection.call("marker.buildScaffoldTree", new Responder(onBuildMarkerTree, onFaultBuildMarkerTree), scaff_obj.scaff_id);
			
			//this.setStyle("backgroundColor", 0xff0000);
			//Alert.show(String(interval) + " " + String(length) + " " + String(this.width));
			prepare(from, to - from);
		}
		
		/**
		 * 
		 */
		private function onBuildTree(data:Object):void
		{
			trace("Zakonczono budowanie drzewa przedzialowego z contigami...");
			trace("Rozpoczeto pobieranie contigow...");
			// Pobranie contigów z serwera aplikacji
			CursorManager.setBusyCursor();
			connection.call("contig.getFromTree", new Responder(drawContigs, onFaultGetContigs), display_from, display_to);
		}
		
		/**
		 * 
		 */
		private function onFaultBuildTree(event:FaultEvent):void
		{
			CursorManager.removeBusyCursor();
			Alert.show("Blad w oknie ScaffoldCanvas przy budowaniu drzewa contigow!");
		}
		
		/**
		 * 
		 */
		private function onBuildMarkerTree(data:Object):void
		{
			trace("Zakonczono budowanie drzewa przedzialowego z markerami...");
			trace("Rozpoczeto pobieranie markerow...");
			// Pobranie markerow z serwera aplikacji
			connection.call("marker.getFromScaffoldTree", new Responder(drawMarkers, onFaultGetMarkers), display_from, display_to);
		}
		
		/**
		 * 
		 */
		private function onFaultBuildMarkerTree(event:FaultEvent):void
		{
			CursorManager.removeBusyCursor();
			Alert.show("Blad w oknie ScaffoldCanvas przy budowaniu drzewa markerow!");
		}
		
		/**
		 * 
		 */
		private function drawContigs(data:Object):void
		{
			trace("Zakonczono pobieranie contigow z drzewa...");
			trace("\n\t\tOdebralem:" + String(data));
			if(data == null)
				return;
			
			var contigs:Array = ArrayUtil.toArray(data);
			
			trace("Nalezy wyswietlic " + String(contigs.length) + " contigow...");
			
			for(var i:int = 0; i < contigs.length; i++)
			{		
				var cont:ContigVO = new ContigVO(contigs[i].id, contigs[i].scaff_id, contigs[i].order, contigs[i].start, contigs[i].end, contigs[i].sequence, contigs[i].length_bp);
				//drawContig(contigs[i]);
				drawContig(cont);
			}
			CursorManager.removeBusyCursor();
		}
		
		/**
		 * 
		 */
		private function drawContig(contig:ContigVO):void
		{
			// Ustawienie odpowiednich parametrow
			var cont_box:Box = new Box();
			var padding_top:int = 30;
			
			cont_box.graphics.beginFill(StyleManager.getColorName(colors[current_color%3]), 0.5);
			
			current_color += 1;
			
			var cont_length:Number = (contig.end - contig.start);
			
			trace("Rysuje contig (" + contig.id + " --> [ " + contig.start + ", " + contig.end + " ]) na pozycji (" + calculateUnitToDraw(contig.start) + ", " + padding_top + ") o dlugosci: " + (cont_length * factor));
			
			// Narysowanie obiektu
			cont_box.graphics.moveTo(0, 0);
			cont_box.graphics.drawRoundRect(calculateUnitToDraw(contig.start), padding_top, cont_length * factor, 30, 10, 10);
			cont_box.graphics.endFill();
			cont_box.useHandCursor = true;
			cont_box.buttonMode = true;
			cont_box.mouseChildren = false;
			cont_box.addEventListener(MouseEvent.CLICK, ContigEvent.informations(contigBoxClickEventHandler, [contig]));
			var tooltip:String = "<font color='#076baa' size='+4'><b>ID: " + String(contig.id) + "</b></font><br>";
			tooltip += "<font color='#076baa' size='+2'>Saffold ID: " + String(contig.scaff_id) + "</font><br>";
			tooltip += "<font color='#076baa' size='+2'>Position start: " + String(contig.start) + " bp</font><br>";
			tooltip += "<font color='#076baa' size='+2'>Position end: " + String(contig.end) + " bp</font><br>";
			tooltip += "<font color='#076baa' size='+2'>Length: " + String(contig.length_bp) + " bp</font><br><br>";
			tooltip += "<font color='#076baa'>Click to see more informations...</font><br>";
			cont_box.toolTip = tooltip;
			this.addChild(cont_box);
			
			if((cont_length * factor) > 50.0)
			{
				// Dodanie napisu nazwy na obiekcie
				var label:Label = new Label();
				label.text = String(contig.id);
				label.setStyle("color", "White");
				label.x = calculateUnitToDraw(contig.start);
				label.y = padding_top;
				this.addChild(label);
			}
		}
		
		/**
		 * 
		 */
		private function onFaultGetContigs(event:FaultEvent):void
		{
			CursorManager.removeBusyCursor();
			Alert.show("Blad w oknie ScaffoldCanvas przy pobieraniu contigow z drzewa!");
		}
		
		/**
		 * 
		 */
		private function drawMarkers(data:Object):void
		{
			trace("Zakonczono pobieranie markerow z drzewa...");
			trace("\n\t\tOdebralem:" + String(data));
			if(data == null)
				return;
			
			var markers:Array = ArrayUtil.toArray(data);
			
			trace("Nalezy wyswietlic " + String(markers.length) + " markerow...");
			
			for(var i:int = 0; i < markers.length; i++)
			{		
				var mark:MarkerVO = new MarkerVO(markers[i].name, markers[i].chr_id, markers[i].pos_cm, markers[i].cont_id, markers[i].contig_start, markers[i].contig_end, markers[i].scaff_id, markers[i].scaffold_start, markers[i].scaffold_end, markers[i].sequence);
				drawMarker(mark);
			}
		}
		
		/**
		 * 
		 */
		private function drawMarker(marker:MarkerVO):void
		{
			// Ustawienie odpowiednich parametrow
			var mark_box:Box = new Box();
			var padding_top:int = 20;
			var marker_height:int = 50;
			
			mark_box.graphics.beginFill(StyleManager.getColorName("#000000"), 0.5);
			
			var mark_length:Number = (marker.scaffold_end - marker.scaffold_start);
			
			trace("Rysuje marker (" + marker.name + " --> [ " + marker.scaffold_start + ", " + marker.scaffold_end + " ]) na pozycji (" + calculateUnitToDraw(marker.scaffold_start) + ", " + padding_top + ") o dlugosci: " + (mark_length * factor));
			
			// Narysowanie obiektu
			mark_box.graphics.moveTo(0, 0);
			mark_box.graphics.drawRoundRect(calculateUnitToDraw(marker.scaffold_start), padding_top, mark_length * factor, marker_height, 10, 10);
			mark_box.graphics.endFill();
			mark_box.useHandCursor = true;
			mark_box.buttonMode = true;
			mark_box.mouseChildren = false;
			mark_box.addEventListener(MouseEvent.CLICK, MarkerEvent.informations(markerBoxClickEventHandler, [marker]));
			var tooltip:String = "<font color='#076baa' size='+4'><b>Name: " + String(marker.name) + "</b></font><br>";
			tooltip += "<font color='#076baa' size='+2'>Contig ID: " + String(marker.cont_id) + "</font><br>";
			tooltip += "<font color='#076baa' size='+2'>Saffold ID: " + String(marker.scaff_id) + "</font><br>";
			tooltip += "<font color='#076baa' size='+2'>Position start (on scaffold): " + String(marker.scaffold_start) + " bp</font><br>";
			tooltip += "<font color='#076baa' size='+2'>Position end (on scaffold): " + String(marker.scaffold_end) + " bp</font><br>";
			tooltip += "<font color='#076baa' size='+2'>Position (on chromosome): " + String(marker.pos_cm) + " cM</font><br><br>";
			tooltip += "<font color='#076baa'>Click to see more informations...</font><br>";
			mark_box.toolTip = tooltip;
			this.addChild(mark_box);
			
			// Dodanie napisu nazwy na obiekcie
			var label:Label = new Label();
			label.text = String(marker.name);
			label.setStyle("color", "Black");
			label.x = calculateUnitToDraw(marker.scaffold_start) - 20;
			label.y = padding_top + marker_height;
			label.useHandCursor = true;
			label.addEventListener(MouseEvent.CLICK, MarkerEvent.informations(markerBoxClickEventHandler, [marker]));
			this.addChild(label);
		}
		
		/**
		 * 
		 */
		private function onFaultGetMarkers(event:FaultEvent):void
		{
			CursorManager.removeBusyCursor();
			Alert.show("Blad w oknie ScaffoldCanvas przy pobieraniu markerow z drzewa!");
		}
		
		/**
		 * 
		 */
		public function drawContigBox():void
		{
			var box:Box = new Box();
			box.graphics.beginFill(0xFFE87C, 0.5);
			box.graphics.drawRect(0, 30, this.width, 30);
			box.graphics.endFill();
			this.addChild(box);
		}
		
		public function drawBox(x:Number, y:Number, width:Number, height:Number):void
		{
			var box:Box = new Box();
			box.graphics.beginFill(0xFFE87C, 0.3);
			// calculateUnitToDraw?
			trace("Rysuje box na pozycji: " + x + "; " + y + "; " + width + "; " + height + " --> " + this.calculateUnitToDraw(x) + "; " + y + "; " + this.calculateUnitToDraw(this.display_from + width) + "; " + this.height);
			trace("Parametry: \nfactor = " + factor + "\ndisplay_from = " + display_from);
			box.graphics.drawRect(this.calculateUnitToDraw(x), y, this.calculateUnitToDraw(this.display_from + width), this.height);
			box.graphics.endFill();
			this.addChild(box);
		}
		
		// -------------------------------------------- FUNKCJE POMOCNICZE ---------------------------------------------
		
		/**
		 * 
		 * @param from:
		 * @param length:
		 */
		public function prepare(from:Number, length:Number):void
		{
			drawVerticalLines(from, length);
			drawContigBox();
		}
		
		/**
		 * 
		 * @param from:
		 * @param length:
		 */
		private function drawVerticalLines(from:Number, length:Number):void
		{
			trace("\tRysuje linie rozpoczynajac od " + from + " na scaffoldzie o szerokosci " + length);
			var lines:Box = new Box();
			var i:int;
			
			var units:Array = ["", "kbp", "mbp"];
			var unit_index:int = 0;
			
			var line_pos:int = length / 10.0;
			
			for (i = 0; i < length; i++)
			{
				if (i%line_pos == 0)
				{
					var label:Label = new Label();
					var pos_num:Number = (from + i);
					if(pos_num > 1000000)
					{
						pos_num /= 1000000;
						unit_index = 2;
					}
					else if(pos_num > 1000)
					{
						pos_num /= 1000;
						unit_index = 1;
					}
					label.text = String((pos_num).toFixed(2)) + String(units[unit_index]);
					label.x = i * interval;
					label.y = POSITIONS_RULER_PADDING_TOP;
					label.setStyle("fontSize", 10);
					this.addChild(label);
					
					lines.graphics.lineStyle(1, 0x858585);
					
					trace("Rysuje linie (" + String(pos_num) + String(units[unit_index]) + ") na pozycji: " + (i * interval));
					
					lines.graphics.moveTo(i * interval, 0);
					lines.graphics.lineTo(i * interval, this.height);
				}
			}
			this.addChild(lines);
		}
				
		/**
		 * 
		 */
		private function onFault(event:FaultEvent):void
		{
			CursorManager.removeBusyCursor();
			Alert.show("Blad w oknie ScaffoldCanvas!");
		}
		
		/**
		 * 
		 */
		public function shiftStart(event:MouseEvent):void
		{
			shift_start = int(calculateUnitToSlider(event.localX));
			this.parent.addEventListener(MouseEvent.MOUSE_MOVE, mouseMoveShiftHandler);
		}
		
		private function mouseMoveShiftHandler(event:MouseEvent):void 
		{
			if(this.is_added == true)
			{
				this.removeChild(shift_end_label);
			}
			
			var shift_size:int = int(calculateUnitToSlider(event.localX)) - shift_start;
			var arrow:String = "<<<";
			var shift_size_str:String = arrow + " " + String(shift_size);
			if(shift_size < 0)
			{
				shift_size = -shift_size;
				arrow = ">>>";
				shift_size_str = String(shift_size) + " " + arrow;
			}
			
			// Dodanie napisu gdzie konczymy
			shift_end_label = new Label();
			shift_end_label.text = String(shift_size_str);
			shift_end_label.setStyle("color", "Black");
			shift_end_label.x = event.localX - 20;
			shift_end_label.y = event.localY;
			this.addChild(shift_end_label);
			
			this.is_added = true;
		}  
		
		/**
		 * 
		 */
		public function shiftStop(event:MouseEvent):void
		{
			this.parent.removeEventListener(MouseEvent.MOUSE_MOVE, mouseMoveShiftHandler);
			this.is_added = false;
			
			var shift:int = int(calculateUnitToSlider(event.localX)) - shift_start;
			dispatchEvent(new ShiftEvent(-shift));
		}
		
		/**
		 * 
		 */
		public function zoomStart(event:MouseEvent):void
		{
			zoom_start_position = event.localX;
			zoom_start = int(calculateUnitToSlider(event.localX));
			
			zoom_box.graphics.clear();
			this.parent.addEventListener(MouseEvent.MOUSE_MOVE, mouseMoveZoomHandler);
			
			// Dodanie napisu skad dokladnie zaczynamy
			var label:Label = new Label();
			label.text = String(zoom_start);
			label.setStyle("color", "Black");
			label.x = event.localX - 20;
			label.y = event.localY;
			this.addChild(label);
		}
		
		private function mouseMoveZoomHandler(event:MouseEvent):void 
		{
			if(this.is_added == true)
			{
				this.removeChild(zoom_box);
				this.removeChild(zoom_end_label);
			}
			
			zoom_box.graphics.clear();
			zoom_box.graphics.beginFill(0x01DF01, 0.5);
			zoom_box.graphics.drawRect(zoom_start_position, 0, event.localX - zoom_start_position, this.height); 
			zoom_box.graphics.endFill();
			this.addChild(zoom_box);
			
			// Dodanie napisu gdzie konczymy
			zoom_end_label = new Label();
			zoom_end_label.text = String(int(calculateUnitToSlider(event.localX)));
			zoom_end_label.setStyle("color", "Black");
			zoom_end_label.x = event.localX - 20;
			zoom_end_label.y = event.localY;
			this.addChild(zoom_end_label);
			
			this.is_added = true;
		}  
		
		/**
		 * 
		 */
		public function zoomStop(event:MouseEvent):void
		{
			this.parent.removeEventListener(MouseEvent.MOUSE_MOVE, mouseMoveZoomHandler);
			this.is_added = false;
			
			var zoom_stop:int = int(calculateUnitToSlider(event.localX));
			dispatchEvent(new ZoomEvent(zoom_start, zoom_stop));
		}
		
		/**
		 * 
		 * @param event:
		 * @param contig:
		 */
		private function contigBoxClickEventHandler(event:MouseEvent, contig:Object):void
		{
			var contig_informations:ContigInformations = new ContigInformations();
			PopUpManager.addPopUp(contig_informations, this, false);
			PopUpManager.centerPopUp(contig_informations);
			contig_informations.init(contig);
		}
		
		/**
		 * 
		 * @param event:
		 * @param marker:
		 */
		private function markerBoxClickEventHandler(event:MouseEvent, marker:Object):void
		{
			var marker_informations:MarkerInformations = new MarkerInformations();
			PopUpManager.addPopUp(marker_informations, this, false);
			PopUpManager.centerPopUp(marker_informations);
			marker_informations.init(marker);
		}
		
		/**
		 * 
		 */
		public function getFactor():Number
		{
			return factor;
		}
		
		// ------------------------------------- OBLICZANIE JEDNOSTEK ---------------------------------
		
		/**
		 * 
		 * @param unit:
		 * @return:
		 */
		private function calculateUnitToDraw(unit:Number):Number
		{
			//trace("\t\t\t\tCalculateUnitToDraw --- UNIT = " + unit + " --- DISPLAY_FROM = " + display_from);
			return (unit - display_from) * factor;		
		}
		
		/**
		 * 
		 * @param unit:
		 * @return:
		 */
		private function calculateUnitToSlider(unit:Number):Number
		{
			return (unit + display_from * factor) / factor;
		}
	}
}