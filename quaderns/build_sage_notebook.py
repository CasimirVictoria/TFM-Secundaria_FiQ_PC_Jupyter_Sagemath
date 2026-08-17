import json

notebook = {
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "# 🚀 Simulador Simbòlic Natiu de Tir Parabòlic 2D i 3D en SageMath\n",
        "### *Modelització Cinemàtica i Càlcul Simbòlic Pur (CAS) sense Discretització Numèrica*\n",
        "**Autor:** Casimir Victòria — *Treball de Final de Màster (Física i Química)*  \n",
        "**Motor:** SageMath (Kernel Simbòlic Natiu `sagemath`)  \n",
        "**Llicència:** Creative Commons Zero 1.0 (CC0 - Domini Públic)  \n",
        "\n",
        "---\n",
        "\n",
        "## 🎯 1. Fonamentació Didàctica i Modelització Simbòlica (LOMLOE)\n",
        "En la didàctica tradicional de la física, l'alumnat sovint queda atrapat en l'aritmètica de taules de valors o en la discretització de vectors numèrics. L'objectiu d'aquest quadern és treballar exclusivament amb **funcions matemàtiques formals contínues** a través del sistema de càlcul simbòlic **SageMath**.\n",
        "\n",
        "Les lleis físiques es defineixen com a equacions algebraiques exactes, es dedueixen analíticament les solucions i es tracen les trajectòries en 2D i 3D directament des de les funcions simbòliques emprant `parametric_plot`, `parametric_plot3d` i `@interact`.\n",
        "\n",
        "---"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 🧮 2. Deducció Simbòlica Exacta de les Lleis del Moviment\n",
        "Definim les variables simbòliques formals de l'espai-temps ($t, x, y, z$) i els paràmetres físics ($v_0, \\theta, g, y_0, w$)."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Variables simbòliques formals de SageMath\n",
        "var('t, g, v0, theta, y0, x, y, z, w')\n",
        "\n",
        "# Equacions paramètriques contínues del moviment\n",
        "x(t) = v0 * cos(theta) * t\n",
        "y(t) = y0 + v0 * sin(theta) * t - (1/2) * g * t^2\n",
        "z(t) = (1/2) * w * t^2  # Modelització 3D d'una acceleració lateral (vent)\n",
        "\n",
        "print(\"📌 Equacions paramètriques formals:\")\n",
        "show(x(t))\n",
        "show(y(t))\n",
        "show(z(t))\n",
        "\n",
        "# 1. Temps de vol simbòlic analític quan y(t) == 0 (amb y0 = 0)\n",
        "sol_t = solve(y(t).subs(y0=0) == 0, t)\n",
        "t_vol = sol_t[0].rhs()\n",
        "\n",
        "# 2. Abast màxim analític reduït trigonomètricament\n",
        "x_max = x(t_vol).trig_reduce()\n",
        "\n",
        "# 3. Altura màxima analítica (quan la velocitat vertical vy == 0)\n",
        "vy(t) = diff(y(t), t)\n",
        "t_pujada = solve(vy(t).subs(y0=0) == 0, t)[0].rhs()\n",
        "y_max = y(t_pujada).subs(y0=0).trig_reduce()\n",
        "\n",
        "print(\"\\n🎯 Resultats simbòlics deduïts analíticament per SageMath:\")\n",
        "pretty_print(html(f\"<b>Temps de vol:</b> ${latex(t_vol)}$\"))\n",
        "pretty_print(html(f\"<b>Abast màxim:</b> ${latex(x_max)}$\"))\n",
        "pretty_print(html(f\"<b>Altura màxima:</b> ${latex(y_max)}$\"))"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 📈 3. Traçat Simbòlic Natiu 2D i 3D (`parametric_plot` & `plot3d`)\n",
        "SageMath traça les corbes contínues directament des de les expressions simbòliques sense cap discretització numèrica manual."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Paràmetres per a la visualització simbòlica\n",
        "v0_val = 25\n",
        "theta_val = pi / 4  # 45 graus\n",
        "g_val = 9.81\n",
        "w_val = 1.5         # component de vent per a la trajectòria 3D\n",
        "\n",
        "t_vol_num = t_vol.subs(v0=v0_val, theta=theta_val, g=g_val)\n",
        "\n",
        "# Gràfica paramètrica simbòlica 2D en SageMath\n",
        "p2d = parametric_plot(\n",
        "    (x(t).subs(v0=v0_val, theta=theta_val),\n",
        "     y(t).subs(v0=v0_val, theta=theta_val, g=g_val, y0=0)),\n",
        "    (t, 0, t_vol_num),\n",
        "    color='blue',\n",
        "    thickness=3,\n",
        "    axes_labels=['Distància $x$ (m)', 'Alçada $y$ (m)'],\n",
        "    title='Trajectòria Parabòlica Simbòlica 2D en SageMath'\n",
        ")\n",
        "show(p2d, gridlines=True)\n",
        "\n",
        "# Gràfica paramètrica simbòlica 3D (amb desviació tridimensional)\n",
        "p3d = parametric_plot3d(\n",
        "    (x(t).subs(v0=v0_val, theta=theta_val),\n",
        "     z(t).subs(w=w_val),\n",
        "     y(t).subs(v0=v0_val, theta=theta_val, g=g_val, y0=0)),\n",
        "    (t, 0, t_vol_num),\n",
        "    color='red',\n",
        "    thickness=4\n",
        ")\n",
        "show(p3d)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 🎮 4. Simulador Interactiu Simbòlic Natiu (`@interact`)\n",
        "L'alumnat pot manipular directament la velocitat, l'angle, l'alçada i la gravetat de diferents cossos celestes de manera completament interactiva."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "@interact\n",
        "def simulador_tir_simbolic(\n",
        "    v0=slider(5.0, 80.0, 1.0, default=25.0, label='Velocitat v₀ (m/s):'),\n",
        "    angle_deg=slider(5.0, 85.0, 1.0, default=45.0, label='Angle θ (°):'),\n",
        "    y0_in=slider(0.0, 50.0, 1.0, default=0.0, label='Alçada y₀ (m):'),\n",
        "    planeta=selector(['🌍 Terra (9.81 m/s²)', '🌕 Lluna (1.62 m/s²)', '🔴 Mart (3.71 m/s²)', '🪐 Júpiter (24.79 m/s²)'], label='Gravetat:')\n",
        "):\n",
        "    g_dict = {\n",
        "        '🌍 Terra (9.81 m/s²)': 9.81,\n",
        "        '🌕 Lluna (1.62 m/s²)': 1.62,\n",
        "        '🔴 Mart (3.71 m/s²)': 3.71,\n",
        "        '🪐 Júpiter (24.79 m/s²)': 24.79\n",
        "    }\n",
        "    g_num = g_dict[planeta]\n",
        "    theta_rad = angle_deg * pi / 180\n",
        "    \n",
        "    # Resolució simbòlica del temps d'impacte exacte\n",
        "    eq_imp = y(t).subs(v0=v0, theta=theta_rad, g=g_num, y0=y0_in) == 0\n",
        "    sols = solve(eq_imp, t)\n",
        "    t_imp = [s.rhs() for s in sols if s.rhs().n() > 0][0]\n",
        "    \n",
        "    # Avaluació simbòlica de l'abast i altura màxima\n",
        "    x_final = x(t_imp).subs(v0=v0, theta=theta_rad)\n",
        "    t_pujada_num = (v0 * sin(theta_rad) / g_num)\n",
        "    h_max_num = y(t_pujada_num).subs(v0=v0, theta=theta_rad, g=g_num, y0=y0_in)\n",
        "    \n",
        "    # Traçat simbòlic directe\n",
        "    grafic = parametric_plot(\n",
        "        (x(t).subs(v0=v0, theta=theta_rad),\n",
        "         y(t).subs(v0=v0, theta=theta_rad, g=g_num, y0=y0_in)),\n",
        "        (t, 0, t_imp),\n",
        "        color='blue',\n",
        "        thickness=3,\n",
        "        axes_labels=['Distància $x$ (m)', 'Alçada $y$ (m)'],\n",
        "        title=f'Simulació Simbòlica: {planeta} | v₀={v0} m/s, θ={angle_deg}°'\n",
        "    )\n",
        "    \n",
        "    punt_ini = point((0, y0_in), color='green', size=40)\n",
        "    punt_hmax = point((x(t_pujada_num).subs(v0=v0, theta=theta_rad), h_max_num), color='red', size=40)\n",
        "    punt_imp = point((x_final, 0), color='black', size=40)\n",
        "    \n",
        "    show(grafic + punt_ini + punt_hmax + punt_imp, gridlines=True)\n",
        "    \n",
        "    pretty_print(html(f'''\n",
        "    <div style=\"background-color:#f8f9fa; padding:10px; border-left:4px solid #0d6efd; margin-top:10px;\">\n",
        "      <b>📊 Resultats Simbòlics Exactes de la Modelització:</b><br>\n",
        "      • <b>Temps total de vol:</b> {t_imp.n(digits=4)} s<br>\n",
        "      • <b>Alçada màxima:</b> {h_max_num.n(digits=4)} m (als {t_pujada_num.n(digits=4)} s)<br>\n",
        "      • <b>Abast horitzontal:</b> {x_final.n(digits=4)} m<br>\n",
        "    </div>\n",
        "    '''))"
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "SageMath 10.10",
      "language": "sage",
      "name": "sagemath"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "sage",
      "nbformat": 4,
      "nbformat_minor": 4
    }
  },
  "nbformat": 4,
  "nbformat_minor": 4
}

with open('/home/casimir/Documents/Segon_Cervell/TFM/quaderns/01_simulador_tir_parabolic.ipynb', 'w', encoding='utf-8') as f:
  json.dump(notebook, f, indent=2, ensure_ascii=False)
