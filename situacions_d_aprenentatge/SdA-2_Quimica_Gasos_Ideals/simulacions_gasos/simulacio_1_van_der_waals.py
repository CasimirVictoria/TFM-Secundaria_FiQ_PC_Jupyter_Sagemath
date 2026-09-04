"""
Simulació 1: Modelització de Gasos Reals (Van der Waals) vs Gas Ideal
---------------------------------------------------------------------
Explora les isotermes de Van der Waals, l'aparició de la zona de coexistència líquid-vapor,
la comparació amb el Gas Ideal, i la determinació exacta del Punt Crític (Pc, Vc, Tc).

Genera un informe interactiu en HTML autònom amb Plotly.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Constants físiques
R = 0.082057  # atm·L / (mol·K)

# Paràmetres de Van der Waals per a diversos gasos reals [a (atm·L^2/mol^2), b (L/mol), Nom, Tc_exp (K), Pc_exp (atm)]
GASES = {
    'CO2': {
        'name': 'Dioxid de Carboni (CO₂)',
        'a': 3.592,
        'b': 0.04267,
        'color': '#EF553B',
        'desc': 'Gas amb fortes interaccions intermoleculars. Punt crític accessible a T ≈ 31 °C.'
    },
    'H2O_vap': {
        'name': 'Vapor d\'Aigua (H₂O)',
        'a': 5.464,
        'b': 0.03049,
        'color': '#636EFA',
        'desc': 'Forts ponts d\'hidrogen, valors elevats de "a" i temperatura crítica alta.'
    },
    'N2': {
        'name': 'Nitrogen (N₂)',
        'a': 1.390,
        'b': 0.03913,
        'color': '#00CC96',
        'desc': 'Gas apolar amb interaccions dèbils tipus dispersió de London.'
    },
    'He': {
        'name': 'Heli (He)',
        'a': 0.0341,
        'b': 0.0237,
        'color': '#AB63FA',
        'desc': 'Gas noble pràcticament ideal; interaccions quasi nul·les.'
    }
}

def p_vdw(v, t, a, b, n=1.0):
    """Pressió segons l'equació d'estat de Van der Waals."""
    return (n * R * t) / (v - n * b) - (a * n**2) / (v**2)

def p_ideal(v, t, n=1.0):
    """Pressió segons l'equació del Gas Ideal."""
    return (n * R * t) / v

def build_vdw_simulation_html(output_filename="simulacio_1_van_der_waals.html"):
    gas_key = 'CO2'
    gas = GASES[gas_key]
    a, b = gas['a'], gas['b']
    
    # Càlcul analític del punt crític a partir de les derivades de Van der Waals:
    # dP/dV = 0 i d2P/dV2 = 0  =>  Vc = 3b, Tc = 8a / (27 R b), Pc = a / (27 b^2)
    vc = 3.0 * b
    tc = (8.0 * a) / (27.0 * R * b)
    pc = a / (27.0 * (b**2))
    
    # Rangs de volum molar (L/mol)
    v = np.linspace(1.05 * b, 1.2, 800)
    
    # Temperatures a avaluar (en fracció de Tc: subcrítiques, crítica i supercrítiques)
    t_factors = [0.85, 0.92, 1.0, 1.10, 1.25, 1.50]
    temperatures = [f * tc for f in t_factors]
    temp_colors = ['#1f77b4', '#17becf', '#e377c2', '#d62728', '#ff7f0e', '#bcbd22']
    
    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.65, 0.35],
        subplot_titles=(
            f"<b>Diagrama P-V: Isotermes de Van der Waals vs Gas Ideal ({gas['name']})</b>",
            "<b>Diferència Relativa (% d'error del Gas Ideal)</b>"
        ),
        specs=[[{"type": "xy"}, {"type": "xy"}]]
    )
    
    # 1. Traçat de les isotermes de Van der Waals i Ideal
    for i, (temp, col) in enumerate(zip(temperatures, temp_colors)):
        p_v = p_vdw(v, temp, a, b)
        p_id = p_ideal(v, temp)
        
        # Filtrem valors asimptòtics no físics molt alts per a visualització neta
        valid = (p_v > -20) & (p_v < 150)
        v_sub = v[valid]
        p_v_sub = p_v[valid]
        p_id_sub = p_id[valid]
        
        is_critical = np.isclose(temp, tc, atol=0.5)
        label_vdw = f"T = {temp:.1f} K ({temp - 273.15:.1f} °C)" + (" [CRÍTICA Tc]" if is_critical else "")
        
        # Isoterma Van der Waals
        fig.add_trace(
            go.Scatter(
                x=v_sub, y=p_v_sub,
                mode='lines',
                name=label_vdw,
                line=dict(color=col, width=3.5 if is_critical else 2.0, dash='solid' if not is_critical else 'solid'),
                hovertemplate="<b>Van der Waals</b><br>V: %{x:.3f} L/mol<br>P: %{y:.2f} atm<br>T: " + f"{temp:.1f} K<extra></extra>"
            ),
            row=1, col=1
        )
        
        # Isoterma Gas Ideal (línia discontínua)
        fig.add_trace(
            go.Scatter(
                x=v_sub, y=p_id_sub,
                mode='lines',
                name=f"Ideal T={temp:.0f}K",
                line=dict(color=col, width=1.2, dash='dot'),
                showlegend=False,
                hovertemplate="<b>Gas Ideal</b><br>V: %{x:.3f} L/mol<br>P: %{y:.2f} atm<extra></extra>"
            ),
            row=1, col=1
        )
        
        # 2. Subplot d'error relatiu: (P_ideal - P_vdw) / P_vdw * 100
        # Prenem un rang amb P > 0
        v_err = np.linspace(1.2 * b, 0.8, 200)
        p_v_err = p_vdw(v_err, temp, a, b)
        p_id_err = p_ideal(v_err, temp)
        err_pct = ((p_id_err - p_v_err) / p_v_err) * 100
        valid_err = (p_v_err > 1.0) & (np.abs(err_pct) < 150)
        
        fig.add_trace(
            go.Scatter(
                x=v_err[valid_err], y=err_pct[valid_err],
                mode='lines',
                name=f"Error T={temp:.0f}K",
                line=dict(color=col, width=1.8),
                showlegend=False,
                hovertemplate="V: %{x:.3f} L/mol<br>Desviació: %{y:.1f} %<extra></extra>"
            ),
            row=1, col=2
        )

    # Marcador del Punt Crític
    fig.add_trace(
        go.Scatter(
            x=[vc], y=[pc],
            mode='markers+text',
            name='Punt Crític Experimental / Teòric',
            text=["<b>Punt Crític (Vc, Pc)</b>"],
            textposition="top right",
            marker=dict(color='black', size=12, symbol='star', line=dict(color='yellow', width=1.5)),
            hovertemplate=f"<b>PUNT CRÍTIC</b><br>Vc = 3b = {vc:.4f} L/mol<br>Pc = a/(27b²) = {pc:.2f} atm<br>Tc = 8a/(27Rb) = {tc:.2f} K ({tc-273.15:.1f} °C)<extra></extra>"
        ),
        row=1, col=1
    )
    
    # Anotacions pedagògiques
    fig.add_annotation(
        x=vc*1.8, y=pc*0.4,
        text="<b>Zona de Coexistència Líquid-Vapor</b><br>(Ona d'inestabilitat mecànica dP/dV > 0)",
        showarrow=True, arrowhead=2, arrowsize=1, arrowcolor="#1f77b4",
        ax=40, ay=40,
        bgcolor="#EBF5FB", bordercolor="#2980B9", borderwidth=1,
        row=1, col=1
    )
    
    # Línia P = 0 de referència
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, row=1, col=1)
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, row=1, col=2)

    # Estil i configuració dels eixos
    fig.update_xaxes(title_text="<b>Volum Molar V (L / mol)</b>", range=[0.04, 0.7], gridcolor="#EAEDED", row=1, col=1)
    fig.update_yaxes(title_text="<b>Pressió P (atm)</b>", range=[-10, 130], gridcolor="#EAEDED", row=1, col=1)
    
    fig.update_xaxes(title_text="<b>Volum Molar V (L / mol)</b>", range=[0.05, 0.7], gridcolor="#EAEDED", row=1, col=2)
    fig.update_yaxes(title_text="<b>(P_ideal - P_vdw) / P_vdw (%)</b>", range=[-60, 100], gridcolor="#EAEDED", row=1, col=2)

    fig.update_layout(
        title=dict(
            text=f"<b>Simulació Computacional de Gasos Reals: Equació d'Estat de Van der Waals</b><br><sup>Paràmetres per al {gas['name']}: a = {a} atm·L²/mol², b = {b} L/mol | Línies contínues: Van der Waals | Línies de punts: Gas Ideal</sup>",
            x=0.03, y=0.96
        ),
        template="plotly_white",
        hovermode="closest",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.22,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="#BDC3C7",
            borderwidth=1
        ),
        margin=dict(l=60, r=40, t=110, b=100),
        height=720
    )
    
    # Afegim un panell explicatiu didàctic en HTML al voltant
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ca">
    <head>
        <meta charset="utf-8" />
        <title>Simulació 1: Gasos Reals i Van der Waals</title>
        <style>
            body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 20px; background-color: #F8F9F9; color: #2C3E50; }}
            .card {{ background: white; border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }}
            h1 {{ color: #1A5276; margin-top: 0; }}
            .formula-box {{ background: #EAF2F8; border-left: 5px solid #2980B9; padding: 12px 18px; margin: 15px 0; font-family: monospace; font-size: 1.05rem; }}
            .grid-params {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-top: 10px; }}
            .param-card {{ background: #FBFCFC; border: 1px solid #EAEDED; border-radius: 6px; padding: 10px; }}
            .param-title {{ font-weight: bold; color: #2C3E50; }}
            .badge {{ display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 0.85rem; font-weight: bold; background: #D4EFDF; color: #196F3D; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🔬 Didàctica de la Física i Química: Model de Van der Waals</h1>
            <p>Aquesta simulació interactiva permet explorar com les correccions al model de gas ideal (forces d'atracció intermoleculars <i>a</i> i volum exclòs <i>b</i>) expliquen el comportament real i la liqüefacció dels gasos.</p>
            
            <div class="formula-box">
                <b>Equació de Van der Waals:</b> [ P + a·(n/V)² ] · (V - n·b) = n·R·T<br>
                <b>Punt Crític Analític:</b> V<sub>c</sub> = 3b = {vc:.4f} L/mol | T<sub>c</sub> = 8a / (27·R·b) = {tc:.2f} K ({tc-273.15:.1f} °C) | P<sub>c</sub> = a / (27·b²) = {pc:.2f} atm
            </div>

            <div class="grid-params">
                <div class="param-card">
                    <span class="param-title">Gas Seleccionat:</span> {gas['name']}<br>
                    <span class="badge">a = {a} atm·L²/mol²</span>
                    <span class="badge">b = {b} L/mol</span>
                </div>
                <div class="param-card">
                    <span class="param-title">Interpretació de les corbes:</span><br>
                    • <b>T &lt; Tc:</b> Zona amb pendent positiu dP/dV &gt; 0 (inestabilitat que marca la transició líquid-vapor).<br>
                    • <b>T = Tc:</b> Punt d'inflexió amb tangent horitzontal.<br>
                    • <b>T &gt; Tc:</b> Comportament fluid supercrític.
                </div>
            </div>
        </div>

        <div class="card" style="padding: 10px;">
            {fig.to_html(full_html=False, include_plotlyjs='cdn')}
        </div>
    </body>
    </html>
    """
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Simulació 1 generada correctament a: {output_filename}")

if __name__ == "__main__":
    build_vdw_simulation_html("/home/casimir/Documents/Segon_Cervell/TFM/simulacions_gasos/simulacio_1_van_der_waals.html")
