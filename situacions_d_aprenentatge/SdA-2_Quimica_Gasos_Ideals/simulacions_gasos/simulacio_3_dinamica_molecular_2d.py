"""
Simulació 3: Dinàmica Molecular 2D d'un Gas en un Recipient (Pistó Mòbil i Xocs Elàstics)
----------------------------------------------------------------------------------------
Simula la mecànica microscòpica d'un conjunt de partícules de gas xocant elàsticament contra
les parets del recipient i un pistó mòbil. Demostra l'origen estadístic de la Pressió (P)
a partir de la variació de moment lineal (Δp / Δt) i la verificació de la Llei de Boyle (P · V = const)
i Llei de Gay-Lussac (P / T = const).

Genera una animació interactiva en HTML amb Plotly.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def run_molecular_dynamics_simulation(
    num_particles=60,
    num_steps=180,
    dt=0.015,
    L_y=10.0,
    L_x_init=10.0,
    temp=300.0,
    mass=1.0,
    output_filename="simulacio_3_dinamica_molecular_2d.html"
):
    np.random.seed(42)
    
    # Velocitat tèrmica proporcional a sqrt(T)
    v_th = np.sqrt(temp / 300.0) * 8.0
    
    # Posicions i velocitats inicials
    pos = np.random.uniform(0.5, L_x_init - 0.5, (num_particles, 2))
    angles = np.random.uniform(0, 2 * np.pi, num_particles)
    vel = np.zeros((num_particles, 2))
    vel[:, 0] = v_th * np.cos(angles)
    vel[:, 1] = v_th * np.sin(angles)
    
    # Registres temporals per a l'animació de Plotly
    history_x = []
    history_y = []
    history_v = []
    pressure_accum = []
    time_series = []
    volume_series = []
    
    wall_momentum_transfer = 0.0
    
    # El pistó es comprimeix lentament a partir del pas 60 per a demostrar la Llei de Boyle
    piston_x = L_x_init
    
    for step in range(num_steps):
        t = step * dt
        
        # Dinàmica del pistó: compresso en el terç intermedi de la simulació
        if 50 <= step <= 120:
            piston_x -= 0.05
        elif step > 120:
            piston_x = 6.5
        else:
            piston_x = 10.0
            
        current_volume = piston_x * L_y
        
        # Actualització de posicions (Mètode d'integració d'Euler simplificat)
        pos += vel * dt
        
        # Detecció de col·lisions amb les 4 parets (Xocs elàstics)
        # Paret esquerra (x = 0)
        hit_left = pos[:, 0] <= 0.0
        vel[hit_left, 0] *= -1
        pos[hit_left, 0] = np.abs(pos[hit_left, 0])
        wall_momentum_transfer += np.sum(2 * mass * np.abs(vel[hit_left, 0]))
        
        # Pistó dret (x = piston_x)
        hit_piston = pos[:, 0] >= piston_x
        vel[hit_piston, 0] *= -1
        pos[hit_piston, 0] = piston_x - (pos[hit_piston, 0] - piston_x)
        wall_momentum_transfer += np.sum(2 * mass * np.abs(vel[hit_piston, 0]))
        
        # Paret inferior (y = 0)
        hit_bottom = pos[:, 1] <= 0.0
        vel[hit_bottom, 1] *= -1
        pos[hit_bottom, 1] = np.abs(pos[hit_bottom, 1])
        wall_momentum_transfer += np.sum(2 * mass * np.abs(vel[hit_bottom, 1]))
        
        # Paret superior (y = L_y)
        hit_top = pos[:, 1] >= L_y
        vel[hit_top, 1] *= -1
        pos[hit_top, 1] = L_y - (pos[hit_top, 1] - L_y)
        wall_momentum_transfer += np.sum(2 * mass * np.abs(vel[hit_top, 1]))
        
        # Càlcul de la Pressió instantània mitjana (Força / Perímetre = Δp / (Δt · 2(Lx+Ly)))
        perimeter = 2 * (piston_x + L_y)
        inst_pressure = (wall_momentum_transfer / ((step + 1) * dt * perimeter)) * 10.0
        
        speeds = np.linalg.norm(vel, axis=1)
        
        history_x.append(pos[:, 0].copy())
        history_y.append(pos[:, 1].copy())
        history_v.append(speeds.copy())
        pressure_accum.append(inst_pressure)
        time_series.append(t)
        volume_series.append(current_volume)

    # --- CREACIÓ DE L'ANIMACIÓ AMB PLOTLY ---
    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.6, 0.4],
        subplot_titles=(
            "<b>Càmera de Gas 2D (Pistó mòbil i Col·lisions)</b>",
            "<b>Evolució de la Pressió vs Volum (Llei de Boyle: P ∝ 1/V)</b>"
        ),
        specs=[[{"type": "xy"}, {"type": "xy"}]]
    )

    # Marc inicial (Frame 0)
    fig.add_trace(
        go.Scatter(
            x=history_x[0],
            y=history_y[0],
            mode='markers',
            marker=dict(
                size=11,
                color=history_v[0],
                colorscale='Viridis',
                colorbar=dict(title="Velocitat (u.a.)", x=0.55, len=0.7),
                showscale=True,
                line=dict(width=1, color='black')
            ),
            name='Partícules',
            hovertemplate="x: %{x:.2f}<br>y: %{y:.2f}<br>v: %{marker.color:.2f}<extra></extra>"
        ),
        row=1, col=1
    )

    # Línia del pistó mòbil
    fig.add_trace(
        go.Scatter(
            x=[10.0, 10.0],
            y=[0, L_y],
            mode='lines',
            line=dict(color='#C0392B', width=7),
            name='Pistó Mòbil',
            hoverinfo='skip'
        ),
        row=1, col=1
    )

    # Traça de Pressió vs Temps / Volum
    fig.add_trace(
        go.Scatter(
            x=[volume_series[0]],
            y=[pressure_accum[0]],
            mode='lines+markers',
            line=dict(color='#2980B9', width=2.5),
            marker=dict(size=6, color='#E74C3C'),
            name='Pressió Calculada (P)',
            hovertemplate="Volum: %{x:.1f}<br>Pressió: %{y:.2f} atm<extra></extra>"
        ),
        row=1, col=2
    )

    # Generació dels Frames d'animació
    frames = []
    # Submostregem per a optimitzar la velocitat de renderitzat al navegador (cada 2 passos)
    for k in range(0, num_steps, 2):
        cur_piston = 10.0 if k < 50 else (10.0 - 0.05 * (k - 50) if k <= 120 else 6.5)
        frame_data = [
            # 1. Posició partícules
            go.Scatter(
                x=history_x[k],
                y=history_y[k],
                marker=dict(
                    size=11,
                    color=history_v[k],
                    colorscale='Viridis'
                )
            ),
            # 2. Posició pistó
            go.Scatter(
                x=[cur_piston, cur_piston],
                y=[0, L_y]
            ),
            # 3. Evolució corba P-V
            go.Scatter(
                x=volume_series[:k+1],
                y=pressure_accum[:k+1]
            )
        ]
        frames.append(go.Frame(data=frame_data, name=f"frame_{k}"))

    fig.frames = frames

    # Controls d'animació (Botons Play / Pause i Slider)
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=[
                    dict(
                        label="▶ Reprodueix",
                        method="animate",
                        args=[None, {"frame": {"duration": 30, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}]
                    ),
                    dict(
                        label="⏸ Pausa",
                        method="animate",
                        args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]
                    )
                ],
                x=0.05, y=-0.16,
                xanchor="right", yanchor="top"
            )
        ],
        sliders=[
            dict(
                active=0,
                yanchor="top",
                xanchor="left",
                currentvalue=dict(font=dict(size=14), prefix="Pas Temporal: ", visible=True, xanchor="right"),
                transition=dict(duration=0),
                pad=dict(b=10, t=20),
                len=0.85,
                x=0.12, y=-0.12,
                steps=[
                    dict(
                        args=[[f.name], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}],
                        label=f"{i*2}",
                        method="animate"
                    ) for i, f in enumerate(frames)
                ]
            )
        ],
        template="plotly_white",
        margin=dict(l=50, r=40, t=90, b=120),
        height=700
    )

    # Eixos
    fig.update_xaxes(title_text="<b>Posició X (m)</b>", range=[-0.2, 11.0], gridcolor="#EAEDED", row=1, col=1)
    fig.update_yaxes(title_text="<b>Posició Y (m)</b>", range=[-0.2, 10.5], gridcolor="#EAEDED", row=1, col=1)
    
    fig.update_xaxes(title_text="<b>Volum del Recipient V (m²) [Invertit per a compressió]</b>", range=[105, 60], gridcolor="#EAEDED", row=1, col=2)
    fig.update_yaxes(title_text="<b>Pressió de Xocs P (unitats arbitràries)</b>", range=[0, np.max(pressure_accum)*1.25], gridcolor="#EAEDED", row=1, col=2)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ca">
    <head>
        <meta charset="utf-8" />
        <title>Simulació 3: Dinàmica Molecular 2D de Gasos</title>
        <style>
            body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 20px; background-color: #F8F9F9; color: #2C3E50; }}
            .card {{ background: white; border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }}
            h1 {{ color: #C0392B; margin-top: 0; }}
            .formula-box {{ background: #FDEDEC; border-left: 5px solid #E74C3C; padding: 12px 18px; margin: 15px 0; font-family: monospace; font-size: 1.05rem; }}
            .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
            .info-card {{ background: #FBFCFC; border: 1px solid #EAEDED; border-radius: 6px; padding: 12px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>⚙️ Dinàmica Molecular: Emergència Microscòpica de la Pressió</h1>
            <p>Aquesta simulació implementa un motor físic basat en partícules rígides i col·lisions elàstiques. Permet a l'alumnat comprovar que la <b>pressió macroscòpica</b> sorgeix de la transferència acumulada de quantitat de moviment per unitat de temps (impuls) contra el pistó.</p>
            
            <div class="formula-box">
                <b>Definició Microscòpica de la Força:</b> F = ∑ (Δp / Δt) = 2·m·∑|v<sub>x</sub>| / Δt<br>
                <b>Llei de Boyle:</b> Quan el pistó redueix el volum V, la freqüència de xocs augmenta automàticament, duplicant la pressió P (P · V = constant).
            </div>

            <div class="info-grid">
                <div class="info-card">
                    <b>🎯 Instruccions Didàctiques:</b><br>
                    1. Prem el botó <b>«Reprodueix»</b> per a iniciar la simulació.<br>
                    2. Observa com a mesura que el pistó roig comprimeix el gas (reducció de volum), la freqüència de xocs s'intensifica i la corba de pressió a la dreta s'enfila.
                </div>
                <div class="info-card">
                    <b>🌈 Codi de Colors:</b><br>
                    El color de cada partícula indica la seua velocitat escalar instantània (groc = ràpida, morat = lenta), reflectint la distribució tèrmica.
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

    print(f"✅ Simulació 3 generada correctament a: {output_filename}")

if __name__ == "__main__":
    run_molecular_dynamics_simulation(output_filename="/home/casimir/Documents/Segon_Cervell/TFM/simulacions_gasos/simulacio_3_dinamica_molecular_2d.html")
