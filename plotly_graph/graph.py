import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

class Graph():
    def __init__(self):
        self.marker_style = dict(
            size=8,
            color='blue',
            opacity=0.7
        )


    def line_graph(self, df:pd.DataFrame, x_list:list, y:str = None, agg:str =None ) ->None:

        """라인 그래프"""

        for x in x_list:
            if agg == "count":
                df_plot = df.groupby(x)['cust_num'].count().reset_index(name='value')
            elif agg == "sum":
                df_plot = df.groupby(x)['total_cost_price'].sum().reset_index(name='value')
            elif agg == "count_mix":
                if y is None:
                    raise ValueError("count_mix를 사용하려면 y인자가 필요합니다.")
                df_plot = df.groupby([x,y])["cust_num"].count().reset_index(name='value')
            else:
                raise ValueError("지원되지 않는 집계 방식입니다.")


        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df_plot[x],
                y=df_plot['value'],
                mode='lines+markers+text',
                text = df_plot['value'],
                textposition ='top center',       # 선으로 표시 (mode='lines+markers'로 설정하면 점과 선이 함께 표시)
                line=dict(color='blue', width=2),
                marker=dict(
                    size=10,
                    color='black'
                ),
                name='라인 그래프 데이터',
                showlegend=True
            )
        )

        fig.update_xaxes(
            type = 'category',
            tickmode='linear',    # 선형 tick 모드로 설정
            tickangle=45          # tick 라벨을 45도 기울여 표시 (옵션)
        )

        fig.update_layout(
            title="라인 그래프",
            xaxis_title=x,
            yaxis_title=f"주차별 {agg}"
        )

        fig.show()

    def bar_graph(self, df:pd.DataFrame, x_list:list, y:str = None, agg:str = None) ->None:
        
        for x in x_list:
            if agg == "count":
                df_plot = df.groupby(x)['cust_num'].count().reset_index(name='value')
                chart_type = 'line'
            elif agg == "sum":
                df_plot = df.groupby(x)['total_cost_price'].sum().reset_index(name='value')
                chart_type = 'line'
            elif agg == "count_mix":
                if y is None:
                    raise ValueError("count_mix를 사용하려면 y인자가 필요합니다.")
                df_plot = df.groupby([x,y])["cust_num"].count().reset_index(name='value')
                chart_type = 'group_bar'
            else:
                raise ValueError("지원되지 않는 집계 방식입니다.")
    
            fig = go.Figure()

            if chart_type == 'line':
                #x열 기준으로 내림차순 정렬
                df_plot = df_plot.sort_values(by='value', ascending=False)
                category_order = df_plot[x].tolist()

                fig.add_trace(
                    go.Bar(
                        x=df_plot[x],
                        y=df_plot['value'],
                        text=df_plot['value'],
                        textposition='outside',
                        name='막대 그래프'
                    )
                )

                fig.update_layout(
                    title=f"{x} 기준 막대 그래프",
                    xaxis_title=x,
                    yaxis_title=f"수술 {agg}",
                    xaxis=dict(
                        type='category',
                        tickangle=45,
                        categoryorder='array',
                        categoryarray=category_order
                    )
                )
            elif chart_type == 'group_bar':
                # x별 전체 합 계산 후 병합 → 비율 계산
                df_sum = df_plot.groupby(x)['value'].sum().reset_index(name='total')
                df_plot = pd.merge(df_plot, df_sum, on=x)
                df_plot['ratio'] = df_plot['value'] / df_plot['total']

                # 2. 비율 기준 정렬 (stack 순서 반영용)
                df_plot = df_plot.sort_values(by=[x, 'ratio'], ascending=[True, False])

                # 3. 가장 높은 비율의 항목만 텍스트 표시
                df_plot['text_label'] = np.nan
                mask = df_plot.groupby(x)['ratio'].transform('max') == df_plot['ratio']
                df_plot.loc[mask, 'text_label'] = (df_plot.loc[mask, 'ratio'] * 100).round(1).astype(str) + '%'

                for y_val in df_plot[y].unique():
                    df_filtered = df_plot[df_plot[y] == y_val]
                    fig.add_trace(
                        go.Bar(
                            x=df_filtered[x],
                            y=df_filtered['value'],
                            name=str(y_val),
                            text=df_filtered['text_label'],
                            textposition='inside'
                        )
                    )

                fig.update_layout(
                    title=f"{x} 기준 {y}별 고객 수 (Grouped Bar)",
                    xaxis_title=x,
                    yaxis_title="고객 수 (count)",
                    barmode='stack',  # 그룹 막대
                    xaxis=dict(type='category', tickangle=45),
                    legend_title=y,
                )

            fig.show()

    def scatter_graph(self, df:pd.DataFrame, x:str, y:str) ->None:
        """산점도 그래프"""
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=df[x],
                y=df[y],
                mode='markers',    # 데이터 포인트를 점(marker)으로 표시
                marker=dict(
                    size=8,        # 마커의 크기
                    color='blue',  # 마커의 색상
                    opacity=0.7    # 마커의 투명도 (0: 완전 투명, 1: 불투명)
                ),
                name='산점도 데이터',  # 범례에 표시될 이름
                showlegend=True       # 범례를 항상 표시
            )
        )

        # 레이아웃 설정
        fig.update_layout(
            title="산점도",
            xaxis_title=x,
            yaxis_title=y
        )

        fig.show()

    def histogram_graph(self, df:pd.DataFrame, x:str, y:str) -> None:
        "히스토그램 빈도 구하기"
        fig = go.Figure()

        fig.add_trace(
            go.Histogram(
                x=df[x],
                nbinsx=30,          # 구간 수(빈(bin)의 개수)
                name='히스토그램 데이터',
                showlegend=True
            )
        )

        fig.update_layout(
            title="히스토그램",
            xaxis_title=x,
            yaxis_title="빈도"
        )

        fig.show()

    def pie_graph(self, df:pd.DataFrame, x:str, y:str) -> None:
        "파이차트 그리기"
        fig = go.Figure()

        fig.add_trace(
            go.Pie(
            labels=df[x],          # 각 파이 조각의 라벨로 grade 사용
            values=df[y],        # 각 grade의 개수를 값으로 사용
            textinfo='label+percent',  # 파이 차트 내부에 라벨과 백분율 표시
            insidetextorientation='radial'  # 텍스트 방향을 방사형으로 설정
        ))

        # 레이아웃 업데이트: 그래프 제목 설정
        fig.update_layout(title_text='파이차트')

        fig.show()

    def line_graph_date(self, df:pd.DataFrame, x:str, y:str) -> None:
        
        fig = go.Figure()

        # go.Scatter()를 사용하여 라인 그래프 Trace 추가
        fig.add_trace(
            go.Scatter(
                x=df[x],           # x축: 날짜 행은 datetime 객체이어야 한다.
                y=df[y],        # y축: 'count' 값
                mode='lines', # 선과 마커를 함께 표시
                name='Count'
            )
        )

        # x축에 모든 날짜를 표시하도록 업데이트
        fig.update_xaxes(
            tickformat="%b %d\n%Y",  # 날짜 형식 지정
            dtick="M1",              # 1달 간격으로 눈금 표시 (예: "D1" = 하루, "W1" = 주간, "M1": 매월, "M3": 3개월마다)
            tickangle=45             # 라벨 기울이기
        )

        # 레이아웃 업데이트: 제목 및 축 제목 설정
        fig.update_layout(
            title='Time Series Line Plot (Plotly Graph Objects)',
            xaxis_title='Date',
            yaxis_title='Count'
        )

        # 그래프 출력
        fig.show()

    def heatmap_graph(self, df:pd.DataFrame) -> None:

        doc = df.corr(numeric_only=True)

        fig = go.Figure()

        fig.add_trace(
            go.Heatmap(
                z=doc.values,             # 히트맵에 사용될 데이터 (2D 배열)
                x=doc.columns,            # x축: 컬럼 레이블
                y=doc.index,              # y축: 인덱스 레이블
                colorscale='Viridis',      # 컬러 스케일 설정 (원하는 다른 스케일로 변경 가능)
                colorbar=dict(
                    title="Value"          # 컬러바 제목
                ),
                text=doc.values,          # 각 셀에 실제 데이터 값을 텍스트로 추가
                texttemplate='%{z:.2f}',    # 셀 내부에 소수점 둘째 자리까지 포맷팅하여 표시
                hovertemplate='X: %{x}<br>Y: %{y}<br>Value: %{z:.2f}<extra></extra>'  # hover 시 표시 형식
            )
        )

        # 레이아웃 업데이트: 제목 설정
        fig.update_layout(title="Heatmap (Plotly Graph Objects)")
        fig.show()




# 사용예시

# df = df = pd.read_excel('./2개월 수술데이터.xlsx')
# x축 = 'operation'
# y축 = 'cust_num'
# instance = Graph()
# instance.scatter_graph(df,x축,y축)
