import win32gui
import win32con
# import win32process

def find_hwnd(title):
	def _window_enum_callback(hwnd, hwnds):    
		hwnds.append(hwnd)
	hwnds = []
	win32gui.EnumWindows(_window_enum_callback,hwnds)
	results = []
	for i in range(0,len(hwnds),1):
		text = win32gui.GetWindowText(hwnds[i])
		if text.find(title)>=0:
			results.append(hwnds[i])
	return results

def parent_hwnd(hwnd):
	return(win32gui.GetParent(hwnd))

def min_wnd(hwnds):
	if isinstance(hwnds,int):
		hwnds = [hwnds]
	for i in range(0,len(hwnds),1):
		win32gui.ShowWindow(hwnds[i], win32con.SW_MINIMIZE)

def max_wnd(hwnds):
	if isinstance(hwnds,int):
		hwnds = [hwnds]
	for i in range(0,len(hwnds),1):
		win32gui.ShowWindow(hwnds[i], win32con.SW_MAXIMIZE)	

def restore_wnd(hwnds):
	if isinstance(hwnds,int):
		hwnds = [hwnds]
	for i in range(0,len(hwnds),1):
		win32gui.ShowWindow(hwnds[i], win32con.SW_RESTORE)	
		win32gui.SetForegroundWindow(hwnds[i])
		win32gui.SetActiveWindow(hwnds[i])

def close_wnd(hwnds):
	if isinstance(hwnds,int):
		hwnds = [hwnds]
	for i in range(0,len(hwnds),1):
		win32gui.PostMessage(hwnds[i],win32con.WM_CLOSE,0,0)
		

def move_wnd(hwnds,x,y,w=None,h=None):
	if isinstance(hwnds,int):
		hwnds = [hwnds]
	for i in range(0,len(hwnds),1):
		restore_wnd(hwnds[i])		
		rec = win32gui.GetWindowRect(hwnds[i])
		if w == None:
			w = rec[2]-rec[0]
		if h == None:
			h = rec[3]-rec[1]
		win32gui.MoveWindow(hwnds[i],x,y,w,h,True)

def resize_wnd(hwnds,w,h,x=None,y=None):
	if isinstance(hwnds,int):
		hwnds = [hwnds]
	for i in range(0,len(hwnds),1):
		restore_wnd(hwnds[i])		
		rec = win32gui.GetWindowRect(hwnds[i])
		if x == None:
			x = rec[0]
		if y == None:
			y = rec[1]
		win32gui.MoveWindow(hwnds[i],x,y,w,h,True)

def hwnd_cursor():
	flags, hcursor, (x,y) = win32gui.GetCursorInfo()
	hwnd = win32gui.WindowFromPoint((x,y))
	return hwnd

def main():
	pass
if __name__ == '__main__':
	main()

__all__ = [
'find_hwnd','parent_hwnd','min_wnd','max_wnd','restore_wnd','resize_wnd','close_wnd','move_wnd','hwnd_cursor'
]	
