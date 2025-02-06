Matplotlib 라이브러리
│
├── 모듈 (Module) - matplotlib.pyplot, matplotlib.figure, matplotlib.axes 등
│   │
│   ├── 변수 (Variable) - matplotlib.rcParams 
│   │
│   ├── 함수 (Function) - matplotlib.pyplot.plot(), scatter(), bar() 등
│   │    --파라미터(parameter) - figsize, dpi, linewidth 등
│   ├── 클래스 (Class) - matplotlib.figure.Figure, matplotlib.axes.Axes, matplotilb.lines.Line2D, matplotilb.patches.Rectangle 등
│   │   ├── 속성 (Attribute) - figure.dpi, axes.title 등
│   │   ├── 메서드 (Method) - figure.add_subplot(), axes.set_title() 등
│   │   ├── 객체 (Instance) - fig = Figure() fig는 Figure의 인스턴스, ax = Axes() ax는 Axes의 인스턴스 등
        --- 생성자(constructor) --Figure(figsize=(w,h)), AXes(fig,position) 등
variable : rcParams변수는 Matplotlib의 전역 설정을 담고 있음. 활용예시 import matplotlib print(mpl.rcParams['figure.figsize'])등

Matplotilb 
Matplotilb Class 구조파악중 GPT답변 오류의 정정
✔ matplotlib.pyplot은 객체를 직접 정의하지 않고, Figure, Axes 클래스를 내부적으로 생성하고 관리하는 함수 기반 API임.
✔ matplotlib.pyplot.Figure ❌ → 존재하지 않음
✔ matplotlib.pyplot.Axes ❌ → 존재하지 않음
✔ plt.figure() ✅ → 내부적으로 matplotlib.figure.Figure를 생성
✔ plt.subplots() ✅ → 내부적으로 matplotlib.figure.Figure와 matplotlib.axes.Axes를 생성
➡ 내가 처음에 pyplot이 Figure와 Axes를 포함한다고 한 것은 엄밀히 말하면 잘못된 표현이었고, pyplot은 이를 내부적으로 생성하는 함수 API를 제공하는 역할을 한다고 정정해야 해.


from matplotlib import rcParams
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.text import Text

class Axes:
    """
    The Axes contains most of the figure elements: Axis, Tick, Line2D, Text, etc.

    Attributes:
        xlim (tuple): X축 범위
        ylim (tuple): Y축 범위
        title (str): 그래프 제목
    """

    def __init__(self, fig, rect, facecolor=None):
        """
        Axes 객체를 생성하는 생성자.

        Parameters:
            fig (Figure): Axes가 속할 Figure 객체
            rect (list): [left, bottom, width, height] 좌표
            facecolor (str): 배경색 (기본값: None)
        """
        self.figure = fig  # Axes가 속한 Figure 객체
        self.bbox = rect   # Axes의 위치
        self.facecolor = facecolor if facecolor is not None else rcParams['axes.facecolor']

        # X, Y 축 기본 설정
        self.xlim = (0, 1)
        self.ylim = (0, 1)
        self.title = ""

    def plot(self, *args, **kwargs):
        """
        선 그래프를 그리는 함수.

        Returns:
            Line2D: 선 그래프 객체
        """
        line = Line2D(*args, **kwargs)
        return line

    def set_xlim(self, left=None, right=None):
        """ X축 범위를 설정하는 함수. """
        if left is not None:
            self.xlim = (left, self.xlim[1])
        if right is not None:
            self.xlim = (self.xlim[0], right)

    def set_ylim(self, bottom=None, top=None):
        """ Y축 범위를 설정하는 함수. """
        if bottom is not None:
            self.ylim = (bottom, self.ylim[1])
        if top is not None:
            self.ylim = (self.ylim[0], top)

    def set_title(self, label):
        """ 그래프의 제목을 설정하는 함수. """
        self.title = label


# ✅ 함수 기반 API 제공
_axes_instances = {}  # Axes 객체 저장소 (함수 기반 API 유지)

def create_axes(fig, rect=[0.1, 0.1, 0.8, 0.8], facecolor=None):
    """ Axes 객체를 생성하는 함수 기반 API """
    ax = Axes(fig, rect, facecolor)
    _axes_instances[fig] = ax  # Figure별 Axes 저장
    return ax

def get_current_axes(fig):
    """ 현재 활성화된 Axes 객체를 가져오는 함수 """
    if fig in _axes_instances:
        return _axes_instances[fig]
    return create_axes(fig)  # 없으면 새로 생성

def plot(fig, *args, **kwargs):
    """ 선 그래프를 그리는 함수 기반 API """
    ax = get_current_axes(fig)
    return ax.plot(*args, **kwargs)

def set_xlim(fig, left=None, right=None):
    """ X축 범위를 설정하는 함수 기반 API """
    ax = get_current_axes(fig)
    ax.set_xlim(left, right)

def set_ylim(fig, bottom=None, top=None):
    """ Y축 범위를 설정하는 함수 기반 API """
    ax = get_current_axes(fig)
    ax.set_ylim(bottom, top)

def set_title(fig, label):
    """ 그래프의 제목을 설정하는 함수 기반 API """
    ax = get_current_axes(fig)
    ax.set_title(label)

