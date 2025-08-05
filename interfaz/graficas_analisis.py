import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA
import numpy as np

class AnalizadorGraficas:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.df_final = None
        self.cargar_datos()
    
    def cargar_datos(self):
        try:
            # Leer el archivo CSV
            self.df = pd.read_csv(self.csv_path)
            
            # Eliminar columnas no numéricas o que no sean relevantes para el análisis
            columnas_a_eliminar = ['Folder', 'Instance', 'solver']
            for col in columnas_a_eliminar:
                if col in self.df.columns:
                    self.df = self.df.drop(columns=[col])
            
            # Normalizar datos numéricos
            df_numerico = self.df.select_dtypes(include='number')
            scaler = MinMaxScaler()
            df_normalizado = pd.DataFrame(scaler.fit_transform(df_numerico), 
                                      columns=df_numerico.columns)
            
            self.df_final = pd.concat([self.df.drop(columns=df_numerico.columns), 
                                     df_normalizado], axis=1)
            return True
        except Exception as e:
            print(f"Error al cargar datos: {str(e)}")
            return False
    
    def matriz_correlacion(self):
        """Genera matriz de correlación"""
        fig = plt.Figure(figsize=(12, 10), dpi=100)
        ax = fig.add_subplot(111)
        
        # Seleccionar solo columnas numéricas para la matriz de correlación
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        matriz_corr = self.df[numeric_cols].corr()
        
        # Crear el heatmap
        sns.heatmap(matriz_corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax,
                   annot_kws={"size": 8}, cbar_kws={"shrink": 0.8})
        
        ax.set_title('Matriz de Correlación de Características', pad=20)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        fig.tight_layout()
        return fig
    
    def boxplot_tiempos(self, algoritmo='Random min'):
        fig = plt.Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
    
        # Validar que el algoritmo seleccionado exista en los datos
        algoritmos_disponibles = {
        'Random min': 'Random min',
        'Random best': 'Random best',
        'Diff_fastest best-t-min': 'Diff_fastest best-t-min',
        'Diff_fastest min': 'Diff_fastest min'
        }
    
        if algoritmo not in algoritmos_disponibles:
            raise ValueError(f"Algoritmo no válido. Opciones disponibles: {list(algoritmos_disponibles.keys())}")
    
        # Verificar que la columna existe en el dataframe
        columna_algoritmo = algoritmos_disponibles[algoritmo]
        if columna_algoritmo not in self.df.columns:
            raise ValueError(f"El dataframe no contiene la columna '{columna_algoritmo}'")
    
        # Crear el boxplot
        sns.boxplot(data=self.df, x='jobs', y=columna_algoritmo, ax=ax)
    
        ax.set_title(f'Distribución de Tiempos ({algoritmo}) por Número de Trabajos')
        ax.set_xlabel('Número de trabajos')
        ax.set_ylabel(f'Tiempo ({algoritmo})')
        fig.tight_layout()
        return fig
    
    def dispersion_cv_tiempo(self, algoritmo='Random min'):
        """Genera gráfico de dispersión CV vs Tiempo según algoritmo seleccionado"""
        fig = plt.Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        # Validar que el algoritmo seleccionado exista en los datos
        algoritmos_disponibles = {
            'Random min': 'Random min',
            'Random best': 'Random best',
            'Diff_fastest best-t-min': 'Diff_fastest best-t-min',
            'Diff_fastest min': 'Diff_fastest min'
        }
        
        if algoritmo not in algoritmos_disponibles:
            raise ValueError(f"Algoritmo no válido. Opciones disponibles: {list(algoritmos_disponibles.keys())}")
        
        # Verificar que las columnas existen
        columna_algoritmo = algoritmos_disponibles[algoritmo]
        if columna_algoritmo not in self.df.columns or 'cv(pij)' not in self.df.columns:
            raise ValueError(f"El dataframe no contiene las columnas necesarias")
        
        # Verificar si tenemos datos para hue y size
        hue_data = 'machines' if 'machines' in self.df.columns else None
        size_data = 'jobs' if 'jobs' in self.df.columns else None
        
        # Crear el scatterplot solo con los parámetros que existen
        scatter_params = {
            'data': self.df,
            'x': 'cv(pij)',
            'y': columna_algoritmo,
            'ax': ax
        }
        
        if hue_data:
            scatter_params['hue'] = hue_data
        if size_data:
            scatter_params['size'] = size_data
        
        scatter = sns.scatterplot(**scatter_params)
        
        ax.set_title(f'Relación entre Variabilidad y Tiempo ({algoritmo})')
        ax.set_xlabel('Coeficiente de Variación (cv(pij))')
        ax.set_ylabel(f'Tiempo ({algoritmo})')
        
        # Solo mostrar leyenda si hay elementos etiquetados
        handles, labels = ax.get_legend_handles_labels()
        if handles and labels:
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        else:
            # Eliminar leyenda si no hay elementos
            ax.legend_.remove() if hasattr(ax, 'legend_') else None
        
        fig.tight_layout()
        return fig

    def grafico_violin(self, algoritmo='Random min'):
    
        fig = plt.Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
    
        # Validar que el algoritmo seleccionado exista en los datos
        algoritmos_disponibles = {
        'Random min': 'Random min',
        'Random best': 'Random best',
        'Diff_fastest best-t-min': 'Diff_fastest best-t-min',
        'Diff_fastest min': 'Diff_fastest min'
        }
    
        if algoritmo not in algoritmos_disponibles:
            raise ValueError(f"Algoritmo no válido. Opciones disponibles: {list(algoritmos_disponibles.keys())}")
    
        # Verificar que la columna existe
        columna_algoritmo = algoritmos_disponibles[algoritmo]
        if columna_algoritmo not in self.df.columns:
            raise ValueError(f"El dataframe no contiene la columna '{columna_algoritmo}'")
    
        # Crear el violinplot
        sns.violinplot(data=self.df, x='machines', y=columna_algoritmo, ax=ax)
    
        ax.set_title(f'Distribución de Tiempos ({algoritmo}) por Número de Máquinas')
        ax.set_xlabel('Número de Máquinas')
        ax.set_ylabel(f'Tiempo ({algoritmo})')
        fig.tight_layout()
        return fig
    
    def analisis_pca(self):
        try:
            # Preparar datos para PCA (solo columnas numéricas)
            df_num = self.df.select_dtypes(include=[np.number])
            
            # Excluir columnas no relevantes para el PCA
            columnas_excluir = ['Best', 'Cplex', 'rpd', 'time', 'machines', 'jobs']
            columnas_pca = [col for col in df_num.columns if col not in columnas_excluir]
            
            if not columnas_pca:
                raise ValueError("No hay suficientes columnas numéricas para realizar PCA")
                
            # Escalar datos
            scaler = StandardScaler()
            df_scaled = scaler.fit_transform(df_num[columnas_pca])
            
            # Aplicar PCA
            pca = PCA(n_components=2)
            components = pca.fit_transform(df_scaled)
            
            # Crear figura
            fig = plt.Figure(figsize=(10, 8), dpi=100)
            ax = fig.add_subplot(111)
            
            # Verificar si tenemos datos de 'machines' para colorear
            color_data = self.df['machines'] if 'machines' in self.df.columns else None
            
            # Crear scatter plot
            if color_data is not None:
                scatter = ax.scatter(components[:, 0], components[:, 1], 
                                c=color_data, cmap='viridis', alpha=0.7)
                
                # Añadir barra de color solo si usamos colores
                cbar = fig.colorbar(scatter, ax=ax)
                cbar.set_label('Número de Máquinas')
            else:
                scatter = ax.scatter(components[:, 0], components[:, 1], alpha=0.7)
            
            # Añadir porcentaje de varianza explicada
            var_exp = pca.explained_variance_ratio_
            ax.set_title('Análisis PCA (2 Componentes Principales)')
            ax.set_xlabel(f'Componente 1 ({var_exp[0]:.1%} var. explicada)')
            ax.set_ylabel(f'Componente 2 ({var_exp[1]:.1%} var. explicada)')
            
            # Añadir grid para mejor legibilidad
            ax.grid(True, linestyle='--', alpha=0.6)
            
            fig.tight_layout()
            return fig
            
        except Exception as e:
            print(f"Error en PCA: {str(e)}")
            # Devolver figura vacía con mensaje de error
            fig = plt.Figure(figsize=(10, 8), dpi=100)
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, f"Error en PCA:\n{str(e)}", 
                ha='center', va='center')
            return fig
    
    def grafico_lineas(self):
        try:
            fig = plt.Figure(figsize=(12, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            # Verificar que tenemos las columnas necesarias
            metricas = ['Random min', 'Random best', 'Diff_fastest best-t-min', 'Diff_fastest min']
            metricas_disponibles = [m for m in metricas if m in self.df.columns]
            
            if not metricas_disponibles:
                raise ValueError("No hay métricas disponibles para graficar")
                
            if 'machines' not in self.df.columns:
                raise ValueError("No hay datos de número de máquinas")
            
            # Agrupar por número de máquinas
            df_grouped = self.df.groupby('machines')[metricas_disponibles].mean().reset_index()
            
            # Configurar estilos y colores
            estilos = {
                'Random min': {'marker': 'o', 'color': 'blue', 'label': 'Time RM'},
                'Random best': {'marker': 's', 'color': 'green', 'label': 'Time RB'},
                'Diff_fastest best-t-min': {'marker': 'x', 'color': 'red', 'label': 'Time DFB'},
                'Diff_fastest min': {'marker': 'd', 'color': 'purple', 'label': 'Time DFM'}
            }
            
            # Graficar cada métrica disponible
            for metrica in metricas_disponibles:
                sns.lineplot(data=df_grouped, x='machines', y=metrica,
                            marker=estilos[metrica]['marker'],
                            color=estilos[metrica]['color'],
                            label=estilos[metrica]['label'],
                            ax=ax)
            
            # Configurar título y etiquetas
            ax.set_title('Evolución de Tiempos por Número de Máquinas')
            ax.set_xlabel('Número de Máquinas')
            ax.set_ylabel('Tiempo Promedio')
            
            # Añadir grid y leyenda
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend(title='Algoritmos', bbox_to_anchor=(1.05, 1), loc='upper left')
            
            fig.tight_layout()
            return fig
            
        except Exception as e:
            print(f"Error en gráfico de líneas: {str(e)}")
            # Devolver figura vacía con mensaje de error
            fig = plt.Figure(figsize=(12, 6), dpi=100)
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, f"Error en gráfico de líneas:\n{str(e)}", 
                ha='center', va='center')
            return fig