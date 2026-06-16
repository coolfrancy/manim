from manim import *
import yfinance as yf
import numpy as np

class LiveSPYLine2(Scene):
    def construct(self):
        # Download data
        prices = (
            yf.Ticker("SPY")
            .history(start="2020-01-01", end="2025-01-01")["Close"]
            .tolist()
        )

        # Normalize so it fits nicely in the scene
        p_min = min(prices)
        p_max = max(prices)
        norm_prices = [
            (p - p_min) / (p_max - p_min)
            for p in prices
        ]

        axes = Axes(
            x_range=[0, len(prices), len(prices) // 5],
            y_range=[0, 1, 0.2],
            x_length=12,
            y_length=6,
            tips=False,
        )

        self.play(Create(axes))

        tracker = ValueTracker(1)

        def make_graph():
            n = max(2, int(tracker.get_value()))

            points = [
                axes.c2p(i, norm_prices[i])
                for i in range(n)
            ]

            graph = VMobject(
                stroke_color=GREEN,
                stroke_width=4,
            )
            graph.set_points_as_corners(points)
            return graph

        graph = always_redraw(make_graph)

        dot = always_redraw(
            lambda: Dot(
                axes.c2p(
                    int(tracker.get_value()) - 1,
                    norm_prices[
                        max(0, int(tracker.get_value()) - 1)
                    ],
                ),
                color=YELLOW,
                radius=0.06,
            )
        )

        self.add(graph, dot)

        self.play(
            tracker.animate.set_value(len(prices)),
            run_time=10,
            rate_func=linear,
        )

        self.wait()