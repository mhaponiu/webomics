package com.view
{
	import com.config.Config;
	import com.dialog.ScaffoldInformations;
	import com.event.ScaffoldEvent;
	import com.object.AssembInfo;
	import com.remote.RemoteControl;
	import com.style.HTMLToolTip;
	import com.view.DrawingBlock;
	import com.vos.ScaffoldVO;
	
	import flash.events.Event;
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
	import mx.rpc.events.FaultEvent;
	import mx.styles.StyleManager;
	import mx.utils.ArrayUtil;
	
	/**
	 * 
	 * 
	 */
	public class ChromosomeCanvas extends Canvas
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
		private static const POSITIONS_RULER_PADDING_TOP:Number = 1;
		
		/**
		 * 
		 */
		private static const MINIMUM_SCAFF_LEN:Number = 1.0;
		
		/**
		 * 
		*/
		private var position_X:Number;
		
		/**
		 * 
		 */
		private var assembs_positions:Array;
		
		/**
		 * 
		 */
		private var organism_id:int = -1;
		
		// -------------------------------------------------- KONSTRUKTOR ----------------------------------------------
		
		/**
		 * Konstruktor 
		 * @param width:
		 * @param height:
		 * @param from:
		 * @param to:
		 * @param empty:
		 */
		public function ChromosomeCanvas(width:Number, height:Number, from:Number, to:Number, organism_id:int, empty:Boolean)
		{
			// Nawiazanie polaczenia z serwerem aplikacji
			connection = new NetConnection();
			connection.connect(RemoteControl.GATEWAY);
			
			this.organism_id = organism_id;
			
			assembs_positions = new Array();
			
			// Ustawienie menadzera tooltipow
			ToolTipManager.toolTipClass = HTMLToolTip;
			
			// Szerokosc obszaru rysowania
			this.width = width - 30;
			
			// Wysokosc obszaru rysowania
			this.height = height - 30;
			
			// Szerokosci przedzialu
			var length:Number = to - from;
			
			// Obliczenie stalych wartosci
			display_from = from;
			display_to = to;
			position_X = 0.0;

			if(empty == false)
			{
				// Przygotowanie do wyswietlenia informacji
				prepare();
			}
		}
		
		// -------------------------------------------- FUNKCJE POMOCNICZE ---------------------------------------------
		
		/**
		 *  
		 */
		private function findAssemb(assemb_id:uint):AssembInfo
		{
			for(var i:int = 0; i < assembs_positions.length; ++i)
			{
				if(assemb_id == assembs_positions[i].assemb_id)
					return assembs_positions[i];
			}
			
			return null;
		}
		
		
		/**
		 * 
		 */
		public function prepare():void
		{
			// Pobranie informacji o typach asemblacji
			connection.call("chromosome.getAssembsFromOrganism", new Responder(onGetAssembs, onFaultGetAssembs), this.organism_id);
		}
		
		/**
		 *
		 */
		private function onGetAssembs(data:Object):void
		{
			var assembs:ArrayCollection = new ArrayCollection(ArrayUtil.toArray(data));
			
			for(var i:int = 0; i < assembs.length; ++i)
			{
				var ass:AssembInfo = new AssembInfo(assembs[i]['id'], assembs[i]['name'], 20 + 25 * i);
				assembs_positions.push(ass);
			}
			
			// Narysowanie poziomych wskaznikow umiejscowienia scaffoldow
			drawBoxes();
		}
		
		/**
		 * Reakcja na bledne dzialanie komunikacji z serwerem aplikacji 
		 */
		private function onFaultGetAssembs(event:FaultEvent):void
		{
			CursorManager.removeBusyCursor();
			Alert.show(String(event.fault));
		}
		
		/**
		 * 
		 * @param from:
		 * @param length:
		 */
		private function drawVerticalLine(position:Number, real_position:Number):void
		{
			position = this.calculateUnitToDraw(position);
			
			trace("\tRysuje linie (" + real_position + ") dla x = " + position);
			
			var line:Box = new Box();

			var label:Label = new Label();
			label.text = String((real_position).toFixed(2));
			label.x = position;
			label.y = POSITIONS_RULER_PADDING_TOP;
			label.setStyle("fontSize", 10);
			this.addChild(label);
			
			line.graphics.lineStyle(1, 0x858585);
				
			line.graphics.moveTo(position, 0);
			line.graphics.lineTo(position, this.height);

			line.useHandCursor = true;
			line.buttonMode = true;
			line.mouseChildren = false;
			
			var tooltip:String = "<font color='#076baa' size='+4'><b>" + String(real_position) + "</b></font><br>";
			line.toolTip = tooltip;
			
			this.addChild(line);
		}
		
		/**
		 * 
		 * @param scaffolds:
		 */
		public function drawScaffolds(scaffolds:Array):void
		{
			trace("Wszystkich scaffoldow do narysowania: " + scaffolds.length);
			var length:Number = 0.0;
			for(var i:int = 0; i < scaffolds.length; i++)
			{
				var l:Number = (scaffolds[i].end - scaffolds[i].start);
				if(l == 0.0)
					length += MINIMUM_SCAFF_LEN;
				else
					length += (scaffolds[i].end - scaffolds[i].start);
				
				if(i > 0)
				{
					if(scaffolds[i].start != scaffolds[i - 1].end)
						length += (scaffolds[i].start - scaffolds[i - 1].end);	// Dlugosc dziury
				}
			}
			trace("\n\nDlugosc wszystich scaff + dziur: " + length);
			if(length != 0.0)
			{
				interval = this.width / length;
				factor = this.width / length;
				trace("Ilosc scaff: " + scaffolds.length);
				// Rysowanie pojedynczych scaffoldow
				for(var i:int = 0; i < scaffolds.length; i++)
				{	
					if(i > 0)
					{
						if(scaffolds[i].start != scaffolds[i - 1].end)
						{
							this.position_X += (scaffolds[i].start - scaffolds[i - 1].end);	// Przesuwamy sie o dziurke
							this.drawVerticalLine(this.position_X, scaffolds[i].start);
						}
					}
					
					drawScaffold(scaffolds[i]);
					
					var k:Number = (scaffolds[i].end - scaffolds[i].start);
					if(k == 0.0)
					{
						this.position_X += MINIMUM_SCAFF_LEN;	
					}
					else
					{
						this.position_X += (scaffolds[i].end - scaffolds[i].start);
					}
				}
			}
		}
		
		/**
		 * 
		 */
		public function drawBoxes():void
		{
			// Rysujemy tyle kresek ile jest mozliwych typow asemblacji
			
			for(var i:int = 0; i < assembs_positions.length; ++i)
			{
				var box:Box = new Box();
				box.graphics.beginFill(0xFFE87C, 0.5);
				box.graphics.drawRect(0, assembs_positions[i].position, this.width, 20);
				box.graphics.endFill();
				this.addChild(box);
			}
		}
		
		/**
		 * 
		 * @param scaffold:
		 */
		public function drawScaffold(scaffold:Object):void
		{			
			// Ustawienie odpowiednich parametrow
			var scaff:Box = new Box();
			var ass_type:String;
			var padding_top:int;
			
			var assemb:AssembInfo = findAssemb(scaffold.assemb_type);
			if(assemb == null)
			{
				trace("BRAK TYPU ASEMBLACJI:" + String(scaffold.assemb_type));
				return;
			}
		
			padding_top = assemb.position;
			scaff.graphics.beginFill(StyleManager.getColorName(scaffold.color), 1.0);
			ass_type = assemb.name;
			
			var l:Number = (scaffold.end - scaffold.start);
			var scaff_length:Number = 0.0;
			if(l == 0.0)
				scaff_length = MINIMUM_SCAFF_LEN;	
			else
				scaff_length = (scaffold.end - scaffold.start);
			
			trace("Rysuje (" + scaffold.color + ") scaff (" + scaffold.scaff_id + ") na pozycji (" + calculateUnitToDraw(this.position_X) + ", " + padding_top + ") o dlugosci: " + calculateUnitToDraw(scaff_length));
			
			// Narysowanie obiektu
			scaff.graphics.moveTo(0, 0);
			scaff.graphics.drawRoundRect(calculateUnitToDraw(this.position_X) + 1.0, padding_top, calculateUnitToDraw(scaff_length) - 2.0, 20, 10, 10);
			scaff.graphics.endFill();
			scaff.useHandCursor = true;
			scaff.buttonMode = true;
			scaff.mouseChildren = false;
			scaff.doubleClickEnabled = true;
			scaff.addEventListener(MouseEvent.CLICK, ScaffoldEvent.informations(scaffoldBoxClickEventHandler, [scaffold]));
			scaff.addEventListener(MouseEvent.DOUBLE_CLICK, ScaffoldEvent.informations(scaffoldBoxDoubleClickEventHandler, [scaffold]));
			var tooltip:String = "<font color='#076baa' size='+4'><b>ID: " + String(scaffold.scaff_id) + "</b></font><br>";
			tooltip += "<font color='#076baa' size='+2'>Chromosome: " + String(scaffold.chromosome_id) + "</font><br>";
			tooltip += "<font color='#076baa' size='+2'>Assembling: " + String(ass_type) + "</font><br>";
			tooltip += "<font color='#076baa' size='+2'>Position start: " + String(scaffold.start) + " cM</font><br>";
			tooltip += "<font color='#076baa' size='+2'>Position end: " + String(scaffold.end) + " cM</font><br><br>";
			tooltip += "<font color='#076baa'>Click to see structures assigned to this scaffold...</font><br>";
			tooltip += "<font color='#076baa'>Double click to see more informations...</font>";
			scaff.toolTip = tooltip;
			this.addChild(scaff);
			
			if(calculateUnitToDraw(scaff_length) > 50.0)
			{
				// Dodanie napisu nazwy na obiekcie
				var label:Label = new Label();
				label.text = String(scaffold.scaff_id);
				label.setStyle("color", "White");
				label.x = calculateUnitToDraw(this.position_X);
				label.y = padding_top;
				this.addChild(label);
			}
		}
		
		// ------------------------------------------ LISTENERY ---------------------------------------
		
		/**
		 * 
		 * @param event:
		 * @param scaffold:
		 */
		private function scaffoldBoxClickEventHandler(event:MouseEvent, scaffold:Object):void
		{
			this.parentDocument.onScaffoldClicked(scaffold);
		}
		
		/**
		 * 
		 * @param event:
		 * @param scaffold:
		 */
		private function scaffoldBoxDoubleClickEventHandler(event:MouseEvent, scaffold:Object):void
		{
			var scaffold_informations:ScaffoldInformations = new ScaffoldInformations();
			PopUpManager.addPopUp(scaffold_informations, this, false);
			PopUpManager.centerPopUp(scaffold_informations);
			scaffold_informations.init(scaffold);
		}
		
		// ------------------------------------------ RESPONDERY --------------------------------------
		
		/**
		 * 
		*/
		private function drawScaffoldElements(data:Object):void
		{
			
		}
		
		/**
		 * 
		 * @param data:
		 * @return:
		 */
		private function showScaffolds(data:Object):void
		{
			this.drawScaffolds(ArrayUtil.toArray(data))
		}
		
		/**
		 * 
		 */
		private function onFault(event:FaultEvent):void
		{
			CursorManager.removeBusyCursor();
			Alert.show("Blad w oknie ChromosomeCanvas!");
		}
		
		// ------------------------------------- OBLICZANIE JEDNOSTEK ---------------------------------
		
		/**
		 * 
		 * @param unit:
		 * @return:
		 */
		private function calculateUnitToDraw(unit:Number):Number
		{
			//return (unit - display_from) * factor;		
			return unit * factor;		
		}
	}
}