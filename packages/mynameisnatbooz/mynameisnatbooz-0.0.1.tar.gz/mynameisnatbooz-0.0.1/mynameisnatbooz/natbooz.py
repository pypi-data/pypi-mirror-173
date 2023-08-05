class NatbooZ:
	"""
	คลาส NatbooZ คือ
	เป็นข้อมูลเกี่ยวข้องกับ ตัวตนอันยิ่งใหญ่
	ประกอบด้วยยูทูป
	ชื่อช่องยูทูป

	Example
	#----------------

	singto = NatbooZ()
	singto.show_name()
	singto.show_youtube()
	singto.about()
	singto.show_art()
	#----------------
	"""
	def __init__(self):
		self.name = 'สิงโต นำโชค'
		self.page = 'https://www.facebook.com/singtonumchok'


	def show_name(self):
		print('สวัสดีผมชื่อ{}'.format(self.name))

	def show_youtube(self):
		print('https://www.youtube.com/c/SINGTONUMCHOK')

	def about(self):
		text ="""
		--------------------------------
		ชื่อเกิด:	นำโชค ทะนัดรัมย์
		รู้จักในชื่อ:	Jason Mraz เมืองไทย[1]
		เกิด:	26 กรกฎาคม พ.ศ. 2526 (39 ปี)
		ที่เกิด	ไทย: จังหวัดบุรีรัมย์ ประเทศไทย
		แนวเพลง:	ป็อป
		อาชีพ:นักร้องนักแสดงพิธีกรยูทูบเบอร์
		เครื่องดนตรี	:เสียงร้องกีต้าร์อูคูเลเล่
		ช่วงปี	พ.ศ. 2553–ปัจจุบัน
		ค่ายเพลง:	บีลีฟ เรคคอร์ด (2553–2556)
		วอทเดอะดัก: (2556–2563)
		ศิลปินอิสระ: (2564–ปัจจุบัน)
		คู่สมรส	มาเลีย รีเนโรว์
		(2555–ปัจจุบัน)
		--------------------------------
		"""
		print(text)

	def show_art(self):
		text ="""

		("`-''-/").___..--''"`-._ 
		 `6_ 6  )   `-.  (     ).`-.__.`) 
		 (_Y_.)'  ._   )  `._ `. ``-..-' 
		   _..`--'_..-_/  /--'_.'
		  ((((.-''  ((((.'  (((.-' 

		"""
		print(text)

if __name__ == '__main__':
	singto = NatbooZ()
	singto.show_name()
	singto.show_youtube()
	singto.about()
	singto.show_art()

