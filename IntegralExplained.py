from manim import *

class IntegralsExplained(Scene):
    def construct(self):
        # Title Animation
        title = Tex("Integrals Explained", color=PINK).scale(1.2)
        self.play(Write(title), run_time=1.5)
        self.wait(1)
        self.play(title.animate.to_edge(UP), run_time=1.5)

        # Axes and Function
        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 5, 1],
            x_length=5,
            y_length=3,
            axis_config={"include_numbers": False}
        ).shift(DOWN * 0.5)

        labels = axes.get_axis_labels(x_label="x", y_label="y")

        def func(x):
            return 0.3 * (x**2) - 0.8 * x + 1.5  

        graph = axes.plot(func, x_range=[0, 6], color=WHITE)
        func_label = Tex("f(x)", color=WHITE).next_to(graph.get_end(), RIGHT)

        self.play(Create(axes), Write(func_label), Create(graph), Write(labels), run_time=2)
        self.wait(1)

        # Integration limits
        a_val, b_val = 1.5, 5.5
        a = axes.coords_to_point(a_val, 0)
        b = axes.coords_to_point(b_val, 0)
        a_label = Tex("a").next_to(a, DOWN)
        b_label = Tex("b").next_to(b, DOWN)

        a_line = DashedLine(axes.coords_to_point(a_val, 0), axes.coords_to_point(a_val, func(a_val)), color=WHITE)
        b_line = DashedLine(axes.coords_to_point(b_val, 0), axes.coords_to_point(b_val, func(b_val)), color=WHITE)

        self.play(Create(a_line), Create(b_line), Write(a_label), Write(b_label), run_time=1.5)

        # Highlight integral area
        area = axes.get_area(graph, x_range=(a_val, b_val), color=PURPLE_D, opacity=0.7)
        self.play(FadeIn(area), run_time=1)
        self.wait(0.5)

        # Display "Area = ?" text
        area_label = Tex("Area = ?").move_to(area.get_center())
        self.play(Write(area_label), run_time=1)
        self.wait(1)
        self.play(FadeOut(area_label))

        # Display Subdivisions & Summation Formula
        self.last_subdiv_label = None
        self.last_riemann_formula = None

        # **Transform Subdivisions with 0.5 sec transition time**
        for n in [4, 8, 16, 32, 64]:
            self.subdivisions(axes, graph, a_val, b_val, n, transition_time=0.5)

        # Infinite Subdivision
        if self.last_subdiv_label:
            self.play(FadeOut(self.last_subdiv_label, self.last_riemann_formula), run_time=1.5)

        inf_subdiv_label = Tex(r"$\infty$ Subdivisions").move_to(graph.get_center() + UP * 1.5)
        self.play(Write(inf_subdiv_label), run_time=1.5)
        self.wait(1)

        # Display Integral Formula
        integral_formula = MathTex(r"\mathrm{Area} = \int_{a}^{b} f(x) \cdot dx").scale(0.8).next_to(axes, DOWN * 1.5)
        box = SurroundingRectangle(integral_formula, color=GREEN, buff=0.2)

        self.play(Write(integral_formula), Create(box), run_time=2)
        self.wait(3)

    def subdivisions(self, axes, graph, a_val, b_val, num_rectangles, transition_time):
        # Create Riemann Rectangles
        rects = axes.get_riemann_rectangles(
            graph=graph,
            x_range=[a_val, b_val],
            dx=(b_val - a_val) / num_rectangles,
            color=PURPLE_D,
            fill_opacity=0.7
        )

        new_label = Tex(f"{num_rectangles} Subdivisions").move_to(graph.get_center() + UP * 1.5)
        riemann_sum_formula = MathTex(
            rf"\mathrm{{Area}} = \sum_{{i=1}}^{{{num_rectangles}}} f(x_i) \cdot dx"
        ).scale(0.7).next_to(axes, DOWN * 1.5)

        # Transform previous label and rectangles smoothly
        if self.last_subdiv_label:
            self.play(
                ReplacementTransform(self.last_subdiv_label, new_label),
                ReplacementTransform(self.last_riemann_formula, riemann_sum_formula),
                ReplacementTransform(self.last_rects, rects),
                run_time=transition_time  # **Faster transitions (0.5 sec each)**
            )
        else:
            self.play(Write(new_label), Write(riemann_sum_formula), FadeIn(rects), run_time=transition_time)

        self.wait(0.7)

        # Store the last label, formula, and rectangles for the next update
        self.last_subdiv_label = new_label
        self.last_riemann_formula = riemann_sum_formula
        self.last_rects = rects
