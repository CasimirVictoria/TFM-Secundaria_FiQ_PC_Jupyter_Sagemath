"""
Simulació 2: Distribució de Maxwell-Boltzmann i Cinètica Química (Arrhenius)
-----------------------------------------------------------------------------
Visualitza la distribució estadística de velocitats moleculars en gasos, la influència de
la Temperatura (T) i la Massa Molar (M), i connecta amb la Cinètica Química integrant
l'àrea d'energia cinètica superior a l'Energia d'Activació (Ea).

Genera un informe interactiu en HTML autònom amb Plotly.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.integrate import quad

# Constants físiques (SI)
R = 8.314462  # J / (mol·K)
K_B = 1.380649e-23 # J / K
N_A = 6.02214076e23 # mol^-1

GASES_MB = {
    'H2': {'name': 'Hidrogen (H₂)', 'M': 2.016e-3, 'color': '#636EFA'},
    'He': {'name': 'Heli (He)', 'M': 4.0026e-3, 'color': '#EF553B'},
    'N2': {'name': 'Nitrogen (N₂)', 'M': 28.0134e-3, 'color': '#00CC96'},
    'O2': {'name': 'Oxigen (O₂)', 'M': 31.9988e-3, 'color': '#AB63FA'},
    'CO2': {'name': 'Dioxid de Carboni (CO₂)', 'M': 44.01e-3, 'color': '#FFA15A'},
    'Xe': {'name': 'Xenó (Xe)', 'M': 131.293e-3, 'color': '#19D3F3'}
}

def maxwell_boltzmann_pdf(v, T, M):
    """
    Funció de densitat de probabilitat de Maxwell-Boltzmann per a la velocitat v (m/s).
    f(v) = 4 * pi * (M / (2 * pi * R * T))^(3/2) * v^2 * exp(- M * v^2 / (2 * R * T))
    """
    prefactor = 4.0 * np.pi * (M / (2.0 * np.pi * R * T))**(1.5)
    exponent = - (M * (v**2)) / (2.0 * R * T)
    return prefactor * (v**2) * np.exp(exponent)

def build_maxwell_boltzmann_simulation(output_filename="simulacio_2_maxwell_boltzmann.html"):
    v = np.linspace(0, 3500, 1000)
    
    # 1. Efecte de la Temperatura sobre el Nitrogen N2
    gas_ref = GASES_MB['N2']
    M_n2 = gas_ref['M']
    temperatures = [150, 300, 600, 1200]
    t_colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']
    
    # 2. Efecte de la Massa Molar a T = 300 K
    T_const = 300.0
    compare_gases = ['H2', 'He', 'N2', 'Xe']
    
    # 3. Paràmetres per a la reacció química (Energia d'activació Ea en kJ/mol)
    Ea_kJ = 45.0  # 45 kJ/mol
    Ea_J = Ea_kJ * 1e3
    # Velocitat llindar v_act tal que (1/2)*M*v_act^2 = Ea (en J per mol => 1/2 M v^2 = Ea)
    v_act = np.sqrt(2.0 * Ea_J / M_n2)
    
    fig = make_subplots(
        rows=2, cols=2,
        column_widths=[0.5, 0.5],
        row_heights=[0.52, 0.48],
        subplot_titles=(
            f"<b>(A) Efecte de la Temperatura en la distribució de {gas_ref['name']}</b>",
            f"<b>(B) Efecte de la Massa Molecular a T = {T_const:.0f} K</b>",
            "<b>(C) Cinètica Química: Fracció de molècules amb E &gt; Ea (Model d'Arrhenius)</b>",
            "<b>(D) Velocitats Característiques (v_mp, v_mitjana, v_rms)</b>"
        ),
        specs=[
            [{"type": "xy"}, {"type": "xy"}],
            [{"type": "xy"}, {"type": "bar"}]
        ]
    )
    
    # --- SUBPLOT 1: EFECTE TEMPERATURA ---
    for T, col in zip(temperatures, t_colors):
        pdf = maxwell_boltzmann_pdf(v, T, M_n2)
        v_mp = np.sqrt(2.0 * R * T / M_n2)
        v_avg = np.sqrt(8.0 * R * T / (np.pi * M_n2))
        v_rms = np.sqrt(3.0 * R * T / M_n2)
        
        fig.add_trace(
            go.Scatter(
                x=v, y=pdf,
                mode='lines',
                name=f"N₂ a T = {T} K",
                line=dict(color=col, width=2.5),
                hovertemplate=f"<b>N₂ a {T} K</b><br>v: %{{x:.0f}} m/s<br>Densitat: %{{y:.6f}}<br>v_mp: {v_mp:.0f} m/s<br>v_mitj: {v_avg:.0f} m/s<extra></extra>"
            ),
            row=1, col=1
        )
        # Punts de màxima probabilitat (v_mp)
        fig.add_trace(
            go.Scatter(
                x=[v_mp], y=[maxwell_boltzmann_pdf(v_mp, T, M_n2)],
                mode='markers',
                marker=dict(color=col, size=7, symbol='diamond'),
                showlegend=False,
                hoverinfo='skip'
            ),
            row=1, col=1
        )

    # --- SUBPLOT 2: EFECTE MASSA MOLAR ---
    for g_key in compare_gases:
        g_info = GASES_MB[g_key]
        pdf = maxwell_boltzmann_pdf(v, T_const, g_info['M'])
        fig.add_trace(
            go.Scatter(
                x=v, y=pdf,
                mode='lines',
                name=f"{g_info['name']} (M={g_info['M']*1e3:.1f} g/mol)",
                line=dict(color=g_info['color'], width=2.5),
                hovertemplate=f"<b>{g_info['name']} (300 K)</b><br>v: %{{x:.0f}} m/s<br>Probabilitat: %{{y:.6f}}<extra></extra>"
            ),
            row=1, col=2
        )

    # --- SUBPLOT 3: CINÈTICA QUÍMICA I ARRHENIUS ---
    # Comparem T=300 K vs T=600 K amb ombrejat per a v > v_act
    t_arrhenius = [300, 600]
    for T, col in zip(t_arrhenius, ['#2ca02c', '#d62728']):
        pdf = maxwell_boltzmann_pdf(v, T, M_n2)
        fig.add_trace(
            go.Scatter(
                x=v, y=pdf,
                mode='lines',
                name=f"Distribució T={T}K",
                line=dict(color=col, width=2.0),
                showlegend=False,
                hovertemplate=f"v: %{{x:.0f}} m/s<extra></extra>"
            ),
            row=2, col=1
        )
        # Ombrejat d'àrea reactiva (v >= v_act)
        mask_act = v >= v_act
        v_react = v[mask_act]
        pdf_react = pdf[mask_act]
        
        # Càlcul de la fracció reactiva (integral)
        frac, _ = quad(lambda u: maxwell_boltzmann_pdf(u, T, M_n2), v_act, np.inf)
        
        fig.add_trace(
            go.Scatter(
                x=np.concatenate([[v_act], v_react, [v[-1]]]),
                y=np.concatenate([[0], pdf_react, [0]]),
                fill='toself',
                fillcolor=col,
                opacity=0.35,
                line=dict(width=0),
                name=f"Fracció activa (T={T}K): {frac*100:.3f}%",
                hovertemplate=f"T = {T} K: Fracció activa = {frac*100:.4f}%<extra></extra>"
            ),
            row=2, col=1
        )
    
    # Línia d'energia d'activació vertical
    fig.add_vline(
        x=v_act, line_width=2.5, line_dash="dash", line_color="#8E44AD",
        annotation_text=f"<b>v_act (Ea = {Ea_kJ} kJ/mol)</b> = {v_act:.0f} m/s",
        annotation_position="top right",
        row=2, col=1
    )

    # --- SUBPLOT 4: BARRAS COMPARATIVES DE VELOCITATS CARACTERÍSTIQUES ---
    gases_bar = ['H2', 'He', 'N2', 'O2', 'CO2', 'Xe']
    v_mp_list = [np.sqrt(2.0 * R * T_const / GASES_MB[g]['M']) for g in gases_bar]
    v_avg_list = [np.sqrt(8.0 * R * T_const / (np.pi * GASES_MB[g]['M'])) for g in gases_bar]
    v_rms_list = [np.sqrt(3.0 * R * T_const / GASES_MB[g]['M']) for g in gases_bar]
    
    fig.add_trace(
        go.Bar(
            name='v_mp (Més Probable)',
            x=gases_bar, y=v_mp_list,
            marker_color='#3498DB',
            hovertemplate="Gas: %{x}<br>v_mp: %{y:.1f} m/s<extra></extra>"
        ),
        row=2, col=2
    )
    fig.add_trace(
        go.Bar(
            name='v_mitjana (Mitjana)',
            x=gases_bar, y=v_avg_list,
            marker_color='#2ECC71',
            hovertemplate="Gas: %{x}<br>v_mitj: %{y:.1f} m/s<extra></extra>"
        ),
        row=2, col=2
    )
    fig.add_trace(
        go.Bar(
            name='v_rms (Quadràtica Mitjana)',
            x=gases_bar, y=v_rms_list,
            marker_color='#E74C3C',
            hovertemplate="Gas: %{x}<br>v_rms: %{y:.1f} m/s<extra></extra>"
        ),
        row=2, col=2
    )

    # Ajustos dels eixos
    fig.update_xaxes(title_text="<b>Velocitat Molecular v (m / s)</b>", range=[0, 2500], gridcolor="#EAEDED", row=1, col=1)
    fig.update_yaxes(title_text="<b>Densitat f(v) (s / m)</b>", gridcolor="#EAEDED", row=1, col=1)
    
    fig.update_xaxes(title_text="<b>Velocitat Molecular v (m / s)</b>", range=[0, 3200], gridcolor="#EAEDED", row=1, col=2)
    fig.update_yaxes(title_text="<b>Densitat f(v) (s / m)</b>", gridcolor="#EAEDED", row=1, col=2)
    
    fig.update_xaxes(title_text="<b>Velocitat Molecular v (m / s)</b>", range=[0, 2500], gridcolor="#EAEDED", row=2, col=1)
    fig.update_yaxes(title_text="<b>Densitat f(v)</b>", gridcolor="#EAEDED", row=2, col=1)
    
    fig.update_xaxes(title_text="<b>Espècie Química (Gas a 300 K)</b>", gridcolor="#EAEDED", row=2, col=2)
    fig.update_yaxes(title_text="<b>Velocitat (m / s)</b>", gridcolor="#EAEDED", row=2, col=2)

    fig.update_layout(
        title=dict(
            text="<b>Simulació de Teoria Cinètica Molecular: Distribució de Maxwell-Boltzmann i Efecte Arrhenius</b><br><sup>Interacció entre Física Estadística i Cinètica Química per a Batxillerat</sup>",
            x=0.03, y=0.98
        ),
        template="plotly_white",
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="#BDC3C7",
            borderwidth=1
        ),
        margin=dict(l=60, r=40, t=100, b=90),
        height=900
    )

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ca">
    <head>
        <meta charset="utf-8" />
        <title>Simulació 2: Maxwell-Boltzmann i Cinètica Química</title>
        <style>
            body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 20px; background-color: #F8F9F9; color: #2C3E50; }}
            .card {{ background: white; border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }}
            h1 {{ color: #196F3D; margin-top: 0; }}
            .formula-box {{ background: #E8F8F5; border-left: 5px solid #1ABC9C; padding: 12px 18px; margin: 15px 0; font-family: monospace; font-size: 1.05rem; }}
            .key-points {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; }}
            .point-box {{ background: #FBFCFC; border: 1px solid #EAEDED; border-radius: 6px; padding: 12px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🧪 Teoria Cinètica dels Gasos: Maxwell-Boltzmann i Model de Xocs</h1>
            <p>Aquesta simulació connecta la <b>Física Estadística</b> (distribució de velocitats moleculars) amb la <b>Química</b> (Teoria de Col·lisions i Model d'Arrhenius). Permet a l'alumnat comprovar computacionalment com un augment tèrmic multiplica la fracció de molècules amb energia suficient per a reaccionar.</p>
            
            <div class="formula-box">
                <b>Relació de velocitats notables:</b> v<sub>mp</sub> = √(2RT/M) &lt; &lt;v&gt; = √(8RT/πM) &lt; v<sub>rms</sub> = √(3RT/M)<br>
                <b>Fracció de molècules efectives per Arrhenius:</b> f(E &gt; E<sub>a</sub>) ∝ exp(-E<sub>a</sub> / R·T) = Àrea ombrejada en lila
            </div>

            <div class="key-points">
                <div class="point-box">
                    <b>🔥 Efecte Tèrmic (Subplot A):</b><br>
                    En augmentar la temperatura, la corba s'eixampla i s'aplana cap a la dreta (conservant l'àrea total = 1), augmentant dràsticament les molècules d'alta velocitat.
                </div>
                <div class="point-box">
                    <b>⚖️ Efecte de la Massa (Subplot B i D):</b><br>
                    A la mateixa temperatura, els gasos lleugers (H₂, He) es mouen a velocitats molt superiors que els pesants (Xe, CO₂).
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
    
    print(f"✅ Simulació 2 generada correctament a: {output_filename}")

if __name__ == "__main__":
    build_maxwell_boltzmann_simulation("/home/casimir/Documents/Segon_Cervell/TFM/simulacions_gasos/simulacio_2_maxwell_boltzmann.html")
